import base64
import hashlib
import io
import json
import logging
import mimetypes
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx
from mcp.server.fastmcp import FastMCP
from PIL import Image

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
VLM_MODEL = os.environ.get("VLM_MODEL", "minicpm-v")
VLM_TIMEOUT = float(os.environ.get("VLM_TIMEOUT", "180"))
VLM_TEMPERATURE = float(os.environ.get("VLM_TEMPERATURE", "0.1"))
VLM_NUM_PREDICT = int(os.environ.get("VLM_NUM_PREDICT", "8192"))
VLM_NUM_CTX = int(os.environ.get("VLM_NUM_CTX", "32768"))
# ML-team-recommended sampling block. seed pins output for reproducibility,
# repeat_penalty keeps the model from looping, num_batch tunes prompt eval
# throughput on the GPU, num_keep=0 means do not preserve any tokens from a
# previous request in the KV cache.
VLM_TOP_P = float(os.environ.get("VLM_TOP_P", "0.9"))
VLM_TOP_K = int(os.environ.get("VLM_TOP_K", "20"))
VLM_REPEAT_PENALTY = float(os.environ.get("VLM_REPEAT_PENALTY", "1.05"))
# VLM_SEED: integer seed for determinism. Set to "" or unset to omit (Ollama random).
_seed_env = os.environ.get("VLM_SEED", "42").strip()
VLM_SEED: int | None = int(_seed_env) if _seed_env else None
VLM_NUM_BATCH = int(os.environ.get("VLM_NUM_BATCH", "1024"))
VLM_NUM_KEEP = int(os.environ.get("VLM_NUM_KEEP", "0"))
MOCK_MODE = os.environ.get("VISION_MOCK", "1") == "1"
UPSCALE_BELOW_WIDTH = int(os.environ.get("VISION_UPSCALE_BELOW_WIDTH", "400"))
UPSCALE_FACTOR = int(os.environ.get("VISION_UPSCALE_FACTOR", "2"))
MAX_IMAGE_DIMENSION = int(os.environ.get("VISION_MAX_IMAGE_DIMENSION", "0"))

# -- Structured logging (GRACE V-M-* evidence surface) -------------------------
# Default WARNING so existing operators see no behavior change. Set VLM_LOG_LEVEL=INFO
# or DEBUG to surface BLOCK markers required by docs/verification-plan.xml VF-002,
# VF-003, V-M-OLLAMA scenarios. Logger writes to stderr by default to keep stdout
# clean for MCP stdio transport.
VLM_LOG_LEVEL = os.environ.get("VLM_LOG_LEVEL", "WARNING").upper()
_logger = logging.getLogger("vision_sidecar")
if not _logger.handlers:
    _h = logging.StreamHandler()
    _h.setFormatter(logging.Formatter("%(message)s"))
    _logger.addHandler(_h)
_logger.setLevel(getattr(logging, VLM_LOG_LEVEL, logging.WARNING))


def log_call(module: str, fn: str, block: str, level: int = logging.INFO, **fields) -> None:
    """Emit a structured log entry tagged with a GRACE semantic block marker.

    Format: ``[VisionSidecar][module][fn][BLOCK_NAME] k1=v1 k2=v2``.
    Required redaction: callers MUST NOT pass raw base64 image bytes, full Ollama
    response bodies, or env-var values. Pass ``image_sha256``, ``image_size_bytes``,
    ``response_chars`` etc. instead.
    """
    if not _logger.isEnabledFor(level):
        return
    if fields:
        kv = " ".join(f"{k}={v}" for k, v in fields.items())
        _logger.log(level, f"[VisionSidecar][{module}][{fn}][{block}] {kv}")
    else:
        _logger.log(level, f"[VisionSidecar][{module}][{fn}][{block}]")

# qwen3-vl and other reasoning VLMs unconditionally emit <think>...</think>
# tokens before the actual response, consuming the entire num_predict budget on
# dense schema-driven prompts and returning empty `message.content`.
# Confirmed by direct-Ollama matrix on screenshot 03 in eval cycle 2:
# `think: false` (top-level or in options) is silently ignored by Ollama for
# this model. The only working fix is to prefill an assistant turn with the
# closing tag, which makes the model treat thinking as already done and emit
# the response directly. Set VLM_PREFILL_THINKING_CLOSE=0 to disable for
# non-thinking models.
VLM_PREFILL_THINKING_CLOSE = os.environ.get("VLM_PREFILL_THINKING_CLOSE", "1") == "1"

# Hardened extraction-only system prompt. Derived from §7 of the kombo evaluation
# aggregate report (eval_results/kombo/aggregate/aggregate_report.md). Targets the
# stable failure modes the eval surfaced: ✦/+ glyph confusion, FOR-TEACHERS-style
# bulk color hallucinations, missed below-fold clipping, subjective critique
# leakage, and centered-vs-left alignment defaults.
SYSTEM_PROMPT = """You are an extraction-only vision agent for UI and document screenshots.

PRINCIPLES (in priority order):
1. Extraction over interpretation. Report what is visible, not what you infer.
2. No invention. If you cannot read it, say so. Never fill in missing words, hex codes,
   or alignments based on what is "probably" there.
3. Calibrated uncertainty. Mark anything you are not certain about. Volunteer when an
   element appears clipped, partially visible, or below the fold.
4. Per-element attribution. When describing color, weight, or alignment, attach the
   description to a single element. Do not generalize across multiple elements
   (avoid claims like "all section headers are purple") — describe each one separately.
5. Pixel-accurate text. Preserve exact spelling, case, punctuation, glyphs, and
   numbers. Icon characters are visually distinct from the operators they resemble:
   a four-pointed star ✦ is NOT the plus operator +.
   An arrow → is NOT a hyphen -.
   A bullet • is NOT a period.
   Reproduce decorative glyphs exactly as drawn (✦, →, ↗, ◆, ★, ✕, •, ‣).
6. Structure preservation. Mobile line wraps inside a paragraph are NOT sentence
   breaks. Join wrapped lines unless separated by a blank line or a new heading.
7. No subjective critique. Do not call layouts "clean", "intuitive", or "well-designed".
   Do not suggest UX improvements. Report observations only.

OUTPUT POLICY:
- For colors, use qualitative descriptors (light purple, muted grey, white, dark grey).
  Never invent hex codes.
- For alignment, state left/center/right relative to the containing element, only when
  determinable from observed x-positions. Do not default to "centered" when unclear.
- For tables, transcribe the row-label column when present; report row count × column count.
- For viewport screenshots, always state whether content appears clipped at the bottom
  of the viewport.

Return only the requested format. Do not add commentary outside it."""

# Schema description forwarded to the VLM by analyze_structured. Mirrors the schema
# proposed in §8 of the eval report.
STRUCTURED_SCHEMA_HINT = """Return a single JSON object (no markdown fences, no surrounding prose) matching this schema. Use null for unknown fields, [] for empty lists.

{
  "image_type": "webpage_screenshot" | "mobile_screenshot" | "document" | "diagram" | "chart" | "photo" | "ui_mockup" | "other",
  "viewport_class": "desktop" | "tablet" | "mobile" | "small_mobile" | "unknown",
  "visible_text": [
    {
      "block_id": string,
      "role": "heading_h1" | "heading_h2" | "heading_h3" | "eyebrow" | "body" | "label" | "button_label" | "link_text" | "table_cell" | "caption" | "nav",
      "text": string,
      "x_position": "left" | "center" | "right" | "unknown",
      "color_descriptor": string,
      "weight": "bold" | "regular" | "light" | "unknown"
    }
  ],
  "key_ui_elements": [{"kind": string, "label": string, "notes": string}],
  "layout_structure": {
    "columns": "1" | "2" | "3" | "4" | "grid" | "unknown",
    "section_count": integer,
    "ordering": [string]
  },
  "buttons_and_links": [
    {"label": string, "kind": "button" | "link", "primary": boolean, "x_position": "left" | "center" | "right", "row_index": integer}
  ],
  "numbers_dates_amounts": [{"value": string, "context": string}],
  "table_content": {
    "present": boolean,
    "row_count": integer,
    "col_count": integer,
    "header_row": [string],
    "rows": [[string]]
  },
  "glyphs_and_icons": [
    {"in_block": string, "glyph": string, "shape_description": string, "preceding_text": string, "following_text": string}
  ],
  "uncertain_items": [{"block_id": string, "concern": string}],
  "below_fold_or_clipped": {
    "appears_clipped": boolean,
    "evidence": string,
    "expected_missing_elements": [string]
  },
  "interpretation": {"semantic_summary": string, "subjective_notes": string},
  "confidence": {"overall": float, "ocr": float, "color": float, "layout": float}
}

REQUIRED FIELDS:
- "glyphs_and_icons" must list every non-Latin/icon character. If "Earn ✦ Sparks" is visible, emit a glyph entry with the exact ✦ character. Do not transliterate ✦ to + or → to ->.
- "below_fold_or_clipped.appears_clipped" must be true if visible content is structurally incomplete (e.g., a hero with no CTAs, an obviously partial paragraph).
- "color_descriptor" must be qualitative (e.g. "purple", "muted grey", "white"). Hex codes are forbidden.
- Sort "buttons_and_links" by row_index ascending."""

# Per-viewport hint prepended to user prompt when viewport_hint is provided. Targets
# screenshot 10 (small_mobile) clipping miss specifically.
VIEWPORT_HINT_TEXT = {
    "desktop": "Viewport hint: this is a DESKTOP screenshot (~1024px+ wide). Multi-column layouts are likely.",
    "tablet": "Viewport hint: this is a TABLET screenshot. Cards and grids often compress to fewer columns at this width.",
    "mobile": "Viewport hint: this is a MOBILE screenshot (~390px wide). Headlines and CTAs may wrap over multiple lines. Multi-button rows on desktop often wrap to multiple rows here. Content frequently extends below the visible fold.",
    "small_mobile": (
        "Viewport hint: this is a SMALL MOBILE screenshot (~320px wide). Heavy text wrapping is expected. "
        "CRITICAL clipping check: a hero section consists of an eyebrow/heading/subhead PLUS one or more "
        "primary action buttons (e.g. 'Start playing', 'Get started', 'Sign up'). "
        "Buttons in the TOP NAV BAR (e.g. 'Play', 'Login', 'Menu', 'Progress') do NOT count as hero CTAs — "
        "those are navigation, not call-to-action. "
        "If you see a hero heading and subhead but no in-card primary action button below the subhead, "
        "the CTAs are clipped below the visible fold — set appears_clipped=true and list the missing CTAs in "
        "expected_missing_elements. The same applies to any heading whose body or list appears truncated "
        "at the bottom edge of the viewport."
    ),
}

mcp = FastMCP("vision-sidecar", instructions="Vision analysis tools using a local VLM via Ollama. The server applies an extraction-focused system prompt that forbids hex codes, requires per-element color attribution, preserves icon glyphs (✦, →, etc.) verbatim, and flags below-fold clipping. See README.md.")


# -- Mock fixtures (used when VISION_MOCK=1) -----------------------------------

MOCK_ANALYSIS = """## Image Analysis (MOCK)

**Layout:** Single-column page with stacked sections.

**Components detected:**
- Top nav: logo and two pill buttons
- Hero card with eyebrow "READY TO PLAY", H1, subhead, three CTAs
- "No sign-up required" status text below CTAs

**Colors:**
- Background: light purple
- Primary CTA: solid purple
- Secondary CTAs: white with outline

**visible_content_complete: true**

> MOCK response. Set VISION_MOCK=0 to use the real VLM.
"""

MOCK_UI_ANALYSIS = """## UI Component Analysis (MOCK)

### Layout
- Type: vertical stack inside a rounded card
- Width: full container

### Component tree
- Navbar (logo + 2 nav buttons)
- Hero
  - Eyebrow (small purple text)
  - H1 (bold)
  - Subhead (paragraph)
  - 3 CTAs (1 primary + 2 secondary)
  - Status text

**visible_content_complete: true**

> MOCK response. Set VISION_MOCK=0 to use the real VLM.
"""

MOCK_OCR_TEXT = """READY TO PLAY
The math RPG where you build a kingdom
Practice multiplication and division, earn sparks, and grow your kingdom — one kombo at a time.
Start playing  I'm a parent  I'm a teacher
No sign-up required

> MOCK response. Set VISION_MOCK=0 to use the real VLM.
"""

MOCK_TABLE_JSON = {
    "present": True,
    "row_count": 4,
    "col_count": 3,
    "header_row": ["", "kombo", "Prodigy"],
    "rows": [
        ["Scope", "Focused on math facts", "Full curriculum K-8"],
        ["Core skill", "Speed and retention", "Conceptual understanding"],
        ["Complexity", "Start in 5 seconds", "Setup and onboarding"],
        ["Philosophy", "Free, no ads, no paywalls", "Freemium with membership"],
    ],
    "_mock": True,
}

MOCK_STRUCTURED_JSON = {
    "image_type": "webpage_screenshot",
    "viewport_class": "desktop",
    "visible_text": [
        {"block_id": "nav_logo", "role": "nav", "text": "kombo", "x_position": "left", "color_descriptor": "dark grey", "weight": "regular"},
    ],
    "key_ui_elements": [{"kind": "nav", "label": "top nav", "notes": "logo + 2 pill buttons"}],
    "layout_structure": {"columns": "1", "section_count": 1, "ordering": ["nav", "hero"]},
    "buttons_and_links": [],
    "numbers_dates_amounts": [],
    "table_content": {"present": False, "row_count": 0, "col_count": 0, "header_row": [], "rows": []},
    "glyphs_and_icons": [],
    "uncertain_items": [],
    "below_fold_or_clipped": {"appears_clipped": False, "evidence": "all expected hero elements visible", "expected_missing_elements": []},
    "interpretation": {"semantic_summary": "marketing landing hero (mock)", "subjective_notes": ""},
    "confidence": {"overall": 0.9, "ocr": 0.95, "color": 0.7, "layout": 0.85},
    "_mock": True,
}

# v0.3.0: diagnose_error reuses the global SYSTEM_PROMPT (extraction-focused)
# and adds a tool-specific user-prompt block. The ui_diff multi-image gate
# (eval_results/smoke_multi_image/result.md) failed, so a per-tool system
# prompt dispatcher is deferred to v0.4.0+.
DIAGNOSE_ERROR_PROMPT = """Analyze this screenshot which shows an error state, broken layout, or unexpected behavior.

Return a single JSON object (no markdown fences, no surrounding prose) matching this schema:

{
  "error_type": "layout_break" | "missing_element" | "overflow" | "clipping" | "wrong_content" | "error_message" | "crash" | "404" | "console_error" | "validation_error" | "z_index" | "other",
  "description": string (specific: which elements are affected, how they differ from expected),
  "affected_elements": [
    {"label": string, "location": "top-left|top|top-right|center-left|center|center-right|bottom-left|bottom|bottom-right"}
  ],
  "visible_error_text": string | null (transcribed exactly if any error message/code is in the image, else null),
  "suggested_fixes": [string]  (2-3 concrete actionable suggestions, reference CSS properties / HTML structure / responsive breakpoints when applicable),
  "looks_correct": boolean (true ONLY if no error is visible — see rule below),
  "confidence": {"overall": float, "diagnosis": float}
}

Rules:
- If you cannot identify a clear error in the screenshot, set looks_correct=true and emit a minimal payload with error_type="other", empty affected_elements, empty suggested_fixes.
- Do NOT invent error messages that are not visible.
- Do NOT speculate about errors outside the visible viewport (those are clipping concerns, not errors).
- Do NOT critique design choices ("color is too bright") — only report functional errors.
- Color descriptors stay qualitative (no hex)."""

MOCK_DIAGNOSIS = {
    "error_type": "clipping",
    "description": "Hero CTA buttons ('Start playing', 'I'm a parent', 'I'm a teacher') are not visible in the viewport — only the eyebrow, headline, and a partial subhead fit before the bottom edge.",
    "affected_elements": [
        {"label": "Start playing button", "location": "bottom"},
        {"label": "I'm a parent button", "location": "bottom"},
        {"label": "I'm a teacher button", "location": "bottom"},
    ],
    "visible_error_text": None,
    "suggested_fixes": [
        "Reduce hero heading font-size at @media (max-width: 360px) so the H1 wraps to fewer lines.",
        "Add a sticky CTA bar at the bottom of the viewport on small mobile viewports.",
        "Tighten hero card vertical padding when viewport height < 600px.",
    ],
    "looks_correct": False,
    "confidence": {"overall": 0.92, "diagnosis": 0.88},
    "_mock": True,
}


# -- Helpers -------------------------------------------------------------------

def _validate_image(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        log_call("image", "_validate_image", "BLOCK_VALIDATE_IMAGE", level=logging.ERROR, path=str(p), result="not_found")
        raise FileNotFoundError(f"Image not found: {path}")
    size = p.stat().st_size
    if size > 50 * 1024 * 1024:
        log_call("image", "_validate_image", "BLOCK_VALIDATE_IMAGE", level=logging.ERROR, path=str(p), size_bytes=size, result="too_large")
        raise ValueError(f"Image too large: {size / 1024 / 1024:.1f}MB (max 50MB)")

    mime, _ = mimetypes.guess_type(str(p))
    if not mime or not mime.startswith("image/"):
        mime = "image/png"

    log_call("image", "_validate_image", "BLOCK_VALIDATE_IMAGE", path=str(p), size_bytes=size, mime=mime)
    return {
        "path": str(p),
        "size_bytes": size,
        "size_mb": round(size / 1024 / 1024, 2),
        "mime": mime,
        "modified": datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc).isoformat(),
    }


def _preprocess_image(image_bytes: bytes, mime: str) -> tuple[bytes, dict]:
    """Upscale narrow screenshots and/or downscale oversized images.

    Upscale: triggered when image width ≤ UPSCALE_BELOW_WIDTH (default 400px).
    Recommendation §9 of the kombo eval: the 320×568 stress screenshot was the
    dataset's worst case, and the model needs more pixels per character at that
    size to read tight mobile text.

    Downscale: triggered when MAX_IMAGE_DIMENSION > 0 and the longest side of
    the image (after any upscaling) exceeds that limit. Capping prevents VLM
    timeouts on very large images — most VLMs process efficiently below ~1920px.
    """
    try:
        with Image.open(io.BytesIO(image_bytes)) as im:
            orig_w, orig_h = im.size
            info: dict = {"original_size": [orig_w, orig_h]}
            target_w, target_h = orig_w, orig_h

            if orig_w <= UPSCALE_BELOW_WIDTH and UPSCALE_FACTOR > 1:
                target_w = orig_w * UPSCALE_FACTOR
                target_h = orig_h * UPSCALE_FACTOR
                info["upscaled"] = True
                info["upscale_factor"] = UPSCALE_FACTOR
                log_call(
                    "image", "_preprocess_image", "BLOCK_UPSCALE",
                    from_w=orig_w, from_h=orig_h, to_w=target_w, to_h=target_h,
                    factor=UPSCALE_FACTOR, method="Lanczos",
                )

            if MAX_IMAGE_DIMENSION > 0 and max(target_w, target_h) > MAX_IMAGE_DIMENSION:
                scale = MAX_IMAGE_DIMENSION / max(target_w, target_h)
                target_w = max(1, int(target_w * scale))
                target_h = max(1, int(target_h * scale))
                info["downscaled"] = True
                info["downscale_target"] = [target_w, target_h]

            if (target_w, target_h) != (orig_w, orig_h):
                resized = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
                buf = io.BytesIO()
                fmt = "PNG"
                if mime == "image/jpeg":
                    fmt = "JPEG"
                    if resized.mode == "RGBA":
                        resized = resized.convert("RGB")
                resized.save(buf, format=fmt)
                info["final_size"] = [target_w, target_h]
                info["method"] = "Lanczos"
                return buf.getvalue(), info

            return image_bytes, info
    except Exception as e:
        log_call("image", "_preprocess_image", "BLOCK_UPSCALE", level=logging.WARNING, error=str(e), result="skipped")
        return image_bytes, {"preprocess_skipped": True, "error": str(e)}


def _encode_image(path: str) -> tuple[str, str, dict]:
    p = Path(path)
    mime, _ = mimetypes.guess_type(str(p))
    if not mime or not mime.startswith("image/"):
        mime = "image/png"

    with open(p, "rb") as f:
        raw = f.read()

    processed, preprocess_info = _preprocess_image(raw, mime)
    b64 = base64.b64encode(processed).decode("utf-8")
    # Hash the processed bytes (post-upscale) for traceability — never log raw bytes.
    sha = hashlib.sha256(processed).hexdigest()[:16]
    log_call(
        "image", "_encode_image", "BLOCK_ENCODE_IMAGE",
        image_sha256=sha, raw_bytes=len(raw), processed_bytes=len(processed),
        b64_chars=len(b64),
    )
    return b64, mime, preprocess_info


def _call_ollama(
    image_b64: str,
    prompt: str,
    *,
    system_prompt: str = SYSTEM_PROMPT,
    temperature: float = VLM_TEMPERATURE,
    num_predict: int = VLM_NUM_PREDICT,
    response_json: bool = False,
    suppress_thinking: bool | None = None,
) -> str:
    """Send a chat request to Ollama and return `message.content`.

    suppress_thinking: when True (default if VLM_PREFILL_THINKING_CLOSE=1),
    append an assistant turn with content `</think>\n\n` so reasoning models
    (qwen3-vl, other VLMs that emit <think>...</think>) treat their reasoning
    block as already closed and emit the response directly. Without this,
    dense prompts (especially with mobile viewport hints or schema descriptions)
    cause those models to spend the entire num_predict budget on thinking and
    return empty content. Confirmed in eval cycle 2: this single change moved
    `analyze_structured` on screenshots 03/04 from 8/8 empty attempts to
    success in 21s and `analyze_image` neutral on screenshot 07 from
    deterministic empty to success. None = auto (uses VLM_PREFILL_THINKING_CLOSE).
    Set the env var to 0 if you swap to a non-reasoning model.
    """
    if suppress_thinking is None:
        suppress_thinking = VLM_PREFILL_THINKING_CLOSE

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt, "images": [image_b64]},
    ]
    if suppress_thinking:
        messages.append({"role": "assistant", "content": "</think>\n\n"})

    options = {
        "temperature": temperature,
        "num_predict": num_predict,
        "num_ctx": VLM_NUM_CTX,
        "top_p": VLM_TOP_P,
        "top_k": VLM_TOP_K,
        "repeat_penalty": VLM_REPEAT_PENALTY,
        "num_batch": VLM_NUM_BATCH,
        "num_keep": VLM_NUM_KEEP,
    }
    if VLM_SEED is not None:
        options["seed"] = VLM_SEED

    payload = {
        "model": VLM_MODEL,
        "messages": messages,
        "stream": False,
        "options": options,
    }
    if response_json:
        # Ollama supports asking the model to constrain itself to JSON output.
        payload["format"] = "json"

    log_call(
        "ollama", "_call_ollama", "BLOCK_CALL_OLLAMA",
        phase="entry", model=VLM_MODEL, num_predict=num_predict, num_ctx=VLM_NUM_CTX,
        prompt_chars=len(prompt), suppress_thinking=int(bool(suppress_thinking)),
        response_json=int(bool(response_json)),
    )
    _t0 = time.perf_counter()
    try:
        with httpx.Client(timeout=VLM_TIMEOUT) as client:
            resp = client.post(f"{OLLAMA_URL}/api/chat", json=payload)
            resp.raise_for_status()
            data = resp.json()
        content = data.get("message", {}).get("content", "")
        log_call(
            "ollama", "_call_ollama", "BLOCK_CALL_OLLAMA",
            phase="exit", response_chars=len(content),
            wall_seconds=round(time.perf_counter() - _t0, 2),
            status="ok",
        )
        return content
    except httpx.TimeoutException:
        log_call(
            "ollama", "_call_ollama", "BLOCK_CALL_OLLAMA", level=logging.WARNING,
            phase="exit", wall_seconds=round(time.perf_counter() - _t0, 2),
            status="timeout", timeout_seconds=VLM_TIMEOUT,
        )
        return (
            f"[VLM_TIMEOUT] Ollama did not respond within {VLM_TIMEOUT}s. "
            "The image may be too large or the model too slow. "
            "Try increasing VLM_TIMEOUT or setting VISION_MAX_IMAGE_DIMENSION "
            "(e.g. 1920) to cap the longest side."
        )
    except httpx.ConnectError:
        log_call(
            "ollama", "_call_ollama", "BLOCK_CALL_OLLAMA", level=logging.ERROR,
            phase="exit", wall_seconds=round(time.perf_counter() - _t0, 2),
            status="connect_error", url=OLLAMA_URL,
        )
        return (
            f"[VLM_CONNECT_ERROR] Cannot reach Ollama at {OLLAMA_URL}. "
            "Is the Ollama server running?"
        )
    except httpx.HTTPStatusError as exc:
        log_call(
            "ollama", "_call_ollama", "BLOCK_CALL_OLLAMA", level=logging.ERROR,
            phase="exit", wall_seconds=round(time.perf_counter() - _t0, 2),
            status="http_error", http_status=exc.response.status_code,
        )
        return (
            f"[VLM_HTTP_ERROR] Ollama returned HTTP {exc.response.status_code}: "
            f"{exc.response.text[:300]}"
        )


def _try_parse_json(raw: str) -> tuple[object | None, str | None]:
    """Best-effort JSON parse. Strips ```json fences if present. Returns (obj, error)."""
    if not raw:
        log_call("parse", "_try_parse_json", "BLOCK_PARSE_JSON", level=logging.WARNING, result="empty_response")
        return None, "empty response"
    s = raw.strip()
    # Strip a single fenced code block if the model wrapped its output.
    fence = re.match(r"^```(?:json)?\s*(.*?)\s*```$", s, re.DOTALL)
    if fence:
        s = fence.group(1).strip()
    try:
        obj = json.loads(s)
        log_call("parse", "_try_parse_json", "BLOCK_PARSE_JSON", result="ok", path="direct")
        return obj, None
    except json.JSONDecodeError as e:
        # Last-ditch: find the first { and last } and try the slice.
        start = s.find("{")
        end = s.rfind("}")
        if start != -1 and end > start:
            try:
                obj = json.loads(s[start:end + 1])
                log_call("parse", "_try_parse_json", "BLOCK_PARSE_JSON", result="ok", path="brace_fallback")
                return obj, None
            except json.JSONDecodeError:
                pass
        log_call("parse", "_try_parse_json", "BLOCK_PARSE_JSON", level=logging.WARNING, result="parse_error", err=str(e)[:80])
        return None, f"json parse error: {e}"


def _viewport_hint_block(viewport_hint: str | None) -> str:
    if not viewport_hint:
        return ""
    text = VIEWPORT_HINT_TEXT.get(viewport_hint.strip().lower())
    if not text:
        return ""
    return text + "\n\n"


# -- Tools ---------------------------------------------------------------------

@mcp.tool()
def analyze_image(
    image_path: str,
    prompt: str | None = None,
    viewport_hint: str | None = None,
) -> str:
    """Analyze an image using a local vision-language model.

    Sends the image to Ollama VLM and returns a structured text description. Use
    this when you need to understand screenshots, UI mockups, diagrams, or any
    visual content. The server-side system prompt is extraction-focused and
    forbids hex-code invention, subjective critique, and ✦→+ glyph transliteration.

    Args:
        image_path: Absolute path to the image file (PNG, JPEG, GIF, WebP, etc.)
        prompt: Optional custom prompt. Defaults to a general extraction prompt.
        viewport_hint: Optional one of "desktop" | "tablet" | "mobile" | "small_mobile".
            When provided, the server prepends a hint instructing the model to pay
            attention to viewport-specific failure modes (e.g. for "small_mobile"
            this surfaces below-fold clipping detection). Useful when the caller
            knows the capture viewport — pass it!

    Returns:
        JSON string with keys: image (metadata), model, preprocess (upscale info),
        analysis (model output).
    """
    log_call("tools", "analyze_image", "BLOCK_DISPATCH_TOOL", tool_name="analyze_image", viewport_hint=viewport_hint, has_user_prompt=int(prompt is not None))
    meta = _validate_image(image_path)

    if MOCK_MODE:
        return json.dumps({
            "image": meta,
            "model": f"{VLM_MODEL} (MOCK)",
            "prompt": prompt or "default",
            "viewport_hint": viewport_hint,
            "analysis": MOCK_ANALYSIS,
        }, ensure_ascii=False, indent=2)

    image_b64, _, preprocess = _encode_image(image_path)
    user_prompt = (
        _viewport_hint_block(viewport_hint)
        + (prompt or "Describe this image accurately. Extract all visible text, UI elements, layout structure, buttons, labels, numbers, and any visible table content. Mark uncertainty explicitly. Preserve glyphs exactly. State whether content appears clipped at the bottom edge.")
    )
    result = _call_ollama(image_b64, user_prompt)

    return json.dumps({
        "image": meta,
        "model": VLM_MODEL,
        "preprocess": preprocess,
        "viewport_hint": viewport_hint,
        "analysis": result,
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def analyze_ui_screenshot(image_path: str, viewport_hint: str | None = None) -> str:
    """Analyze a UI screenshot and extract component hierarchy.

    Specialized prompt focused on layout, components, and styling — useful for
    frontend handoff. For machine-readable structured output prefer
    `analyze_structured` instead.

    Args:
        image_path: Absolute path to the UI screenshot.
        viewport_hint: Optional viewport class ("desktop"/"tablet"/"mobile"/"small_mobile").
    """
    log_call("tools", "analyze_ui_screenshot", "BLOCK_DISPATCH_TOOL", tool_name="analyze_ui_screenshot", viewport_hint=viewport_hint)
    meta = _validate_image(image_path)

    if MOCK_MODE:
        return json.dumps({
            "image": meta,
            "model": f"{VLM_MODEL} (MOCK)",
            "ui_analysis": MOCK_UI_ANALYSIS,
        }, ensure_ascii=False, indent=2)

    base_prompt = (
        "Analyze this UI screenshot and report:\n"
        "1. Overall layout structure (single column, grid, multi-column).\n"
        "2. Visible components per section (buttons, inputs, cards, links, tables).\n"
        "3. For each text block: role (heading/body/eyebrow/etc.), the text verbatim, "
        "x-position alignment, qualitative color descriptor, font weight.\n"
        "4. Spacing/grouping patterns.\n"
        "5. Any non-Latin glyphs or icon characters (e.g. ✦, →, ◆) — list each separately.\n"
        "6. Whether content appears clipped at the viewport bottom edge.\n"
        "Format as structured markdown. Do not invent hex codes."
    )

    image_b64, _, preprocess = _encode_image(image_path)
    user_prompt = _viewport_hint_block(viewport_hint) + base_prompt
    result = _call_ollama(image_b64, user_prompt)

    return json.dumps({
        "image": meta,
        "model": VLM_MODEL,
        "preprocess": preprocess,
        "viewport_hint": viewport_hint,
        "ui_analysis": result,
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def extract_text_from_image(image_path: str) -> str:
    """Extract text content from an image (OCR-like functionality).

    Transcribes all visible text. Preserves icon glyphs (✦, →, etc.) — does NOT
    transliterate them to ASCII operators.

    Args:
        image_path: Absolute path to the image.
    """
    log_call("tools", "extract_text_from_image", "BLOCK_DISPATCH_TOOL", tool_name="extract_text_from_image")
    meta = _validate_image(image_path)

    if MOCK_MODE:
        return json.dumps({
            "image": meta,
            "model": f"{VLM_MODEL} (MOCK)",
            "extracted_text": MOCK_OCR_TEXT,
        }, ensure_ascii=False, indent=2)

    prompt = (
        "Transcribe ALL text visible in this image exactly as drawn. "
        "Preserve formatting, indentation, line breaks, and structure. "
        "Preserve icon glyphs verbatim (✦ stays ✦, → stays →; do NOT replace with + or ->). "
        "If something is unreadable, write [unreadable] in its place rather than guessing. "
        "Output only the transcribed text, nothing else."
    )

    image_b64, _, preprocess = _encode_image(image_path)
    result = _call_ollama(image_b64, prompt)

    return json.dumps({
        "image": meta,
        "model": VLM_MODEL,
        "preprocess": preprocess,
        "extracted_text": result,
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def extract_table(image_path: str) -> str:
    """Extract a table from a screenshot as JSON (header_row + rows).

    Dedicated table-extraction tool. The kombo evaluation found cell-content OCR
    to be the model's strongest skill (every cell correct across all 6 table runs)
    — this tool surfaces that capability with a clean schema for downstream use.

    The returned JSON includes row labels as the first column when present, so a
    table with row headers ("Scope", "Core skill", ...) and column headers
    ("kombo", "Prodigy") becomes a 4-row × 3-col table where the first column
    holds the row labels and `header_row` starts with an empty string.

    Args:
        image_path: Absolute path to a screenshot containing one table.

    Returns:
        JSON string with keys: image, model, preprocess, table (parsed JSON if
        the model emitted valid JSON, else raw text + parse_error).
    """
    log_call("tools", "extract_table", "BLOCK_DISPATCH_TOOL", tool_name="extract_table")
    meta = _validate_image(image_path)

    if MOCK_MODE:
        return json.dumps({
            "image": meta,
            "model": f"{VLM_MODEL} (MOCK)",
            "table": MOCK_TABLE_JSON,
        }, ensure_ascii=False, indent=2)

    prompt = (
        "Find the single primary table in this screenshot and transcribe it as JSON. "
        "Required schema (no markdown fences, no surrounding prose):\n"
        '{ "present": boolean, "row_count": integer, "col_count": integer, '
        '"header_row": [string], "rows": [[string]] }\n'
        "Rules:\n"
        "- Include the row-label column (e.g. 'Scope', 'Core skill') as the first column. "
        "When the table has both column headers and row labels, the top-left cell is typically empty — "
        "represent it as \"\" in header_row.\n"
        "- Cell text that wraps over multiple lines in the rendered image is ONE string with single spaces "
        "(do not insert newlines).\n"
        "- col_count includes the row-label column.\n"
        "- If no table is present, return {\"present\": false, \"row_count\": 0, \"col_count\": 0, \"header_row\": [], \"rows\": []}.\n"
        "- Preserve numbers and letter grades verbatim ('K-8' stays 'K-8', '5 seconds' stays '5 seconds')."
    )

    image_b64, _, preprocess = _encode_image(image_path)
    raw = _call_ollama(image_b64, prompt, response_json=True, num_predict=VLM_NUM_PREDICT)
    parsed, parse_error = _try_parse_json(raw)

    body: dict = {
        "image": meta,
        "model": VLM_MODEL,
        "preprocess": preprocess,
    }
    if parsed is not None:
        body["table"] = parsed
    else:
        body["table"] = None
        body["raw"] = raw
        body["parse_error"] = parse_error

    return json.dumps(body, ensure_ascii=False, indent=2)


@mcp.tool()
def analyze_structured(image_path: str, viewport_hint: str | None = None) -> str:
    """Return a structured JSON analysis of a screenshot.

    Implements the recommended schema from §8 of the kombo evaluation aggregate
    report. Includes top-level fields specifically targeted at the eval's stable
    failure modes: `glyphs_and_icons` (✦/+ confusion), `below_fold_or_clipped`
    (small-mobile clipping miss), per-block `color_descriptor` (bulk color
    hallucination), and a clearly-fenced `interpretation` block (subjective
    critique leakage).

    Args:
        image_path: Absolute path to the screenshot.
        viewport_hint: Optional one of "desktop" | "tablet" | "mobile" | "small_mobile".
            For "small_mobile" the server prepends an explicit instruction to
            check whether expected hero CTAs are visible, which directly addresses
            the eval's worst-served screenshot.

    Returns:
        JSON string. The `result` key is the parsed structured output if the model
        emitted valid JSON; otherwise raw text + parse_error.
    """
    log_call("tools", "analyze_structured", "BLOCK_DISPATCH_TOOL", tool_name="analyze_structured", viewport_hint=viewport_hint)
    meta = _validate_image(image_path)

    if MOCK_MODE:
        return json.dumps({
            "image": meta,
            "model": f"{VLM_MODEL} (MOCK)",
            "viewport_hint": viewport_hint,
            "result": MOCK_STRUCTURED_JSON,
        }, ensure_ascii=False, indent=2)

    image_b64, _, preprocess = _encode_image(image_path)
    user_prompt = _viewport_hint_block(viewport_hint) + STRUCTURED_SCHEMA_HINT
    raw = _call_ollama(image_b64, user_prompt, response_json=True)
    parsed, parse_error = _try_parse_json(raw)

    body: dict = {
        "image": meta,
        "model": VLM_MODEL,
        "preprocess": preprocess,
        "viewport_hint": viewport_hint,
    }
    if parsed is not None:
        body["result"] = parsed
    else:
        body["result"] = None
        body["raw"] = raw
        body["parse_error"] = parse_error

    return json.dumps(body, ensure_ascii=False, indent=2)


@mcp.tool()
def diagnose_error(
    image_path: str,
    error_context: str | None = None,
    viewport_hint: str | None = None,
) -> str:
    """Analyze a screenshot showing an error and propose actionable fixes.

    Use this when a screenshot contains a visible error state: broken layout,
    error message, console output, crash screen, 404 page, missing element,
    overflow, clipping, validation error, or any UI that does not match
    expected behavior. The model identifies the error, describes what is wrong,
    and suggests concrete fixes.

    Returns the same JSON-payload envelope as `analyze_structured` —
    `result` holds the parsed JSON if the model emitted valid JSON, else
    `raw` + `parse_error`.

    Args:
        image_path: Absolute path to the screenshot showing the error.
        error_context: Optional text from console/terminal/log that provides
            additional context (stack trace, error message). When provided,
            it is included in the user prompt and the model is asked to
            cross-reference it with what is visible.
        viewport_hint: Optional viewport class for responsive-specific analysis.

    Returns:
        JSON string with keys: image, model, preprocess, viewport_hint,
        error_context, result (parsed diagnosis JSON) OR raw + parse_error.
    """
    log_call(
        "tools", "diagnose_error", "BLOCK_DISPATCH_TOOL",
        tool_name="diagnose_error", viewport_hint=viewport_hint,
        has_error_context=int(error_context is not None),
    )
    meta = _validate_image(image_path)

    if MOCK_MODE:
        return json.dumps({
            "image": meta,
            "model": f"{VLM_MODEL} (MOCK)",
            "viewport_hint": viewport_hint,
            "error_context": error_context,
            "result": MOCK_DIAGNOSIS,
        }, ensure_ascii=False, indent=2)

    image_b64, _, preprocess = _encode_image(image_path)

    context_block = ""
    if error_context:
        context_block = (
            "\n\nERROR CONTEXT FROM CONSOLE/LOG:\n```\n"
            + error_context
            + "\n```\nCross-reference this with what you see in the screenshot.\n"
        )

    user_prompt = (
        _viewport_hint_block(viewport_hint)
        + DIAGNOSE_ERROR_PROMPT
        + context_block
    )

    raw = _call_ollama(image_b64, user_prompt, response_json=True)
    parsed, parse_error = _try_parse_json(raw)

    body: dict = {
        "image": meta,
        "model": VLM_MODEL,
        "preprocess": preprocess,
        "viewport_hint": viewport_hint,
        "error_context": error_context,
    }
    if parsed is not None:
        body["result"] = parsed
    else:
        body["result"] = None
        body["raw"] = raw
        body["parse_error"] = parse_error

    return json.dumps(body, ensure_ascii=False, indent=2)


def _resolve_server_version() -> str:
    """Resolve the running source version.

    Priority:
      1. pyproject.toml (project root, sibling of vision_sidecar/) — reflects the
         CURRENT checkout, not a stale install. Most accurate during development.
      2. importlib.metadata for "vision-sidecar-mcp" — used when running from a
         wheel/sdist install with no source pyproject available.
      3. "unknown" fallback.
    """
    try:
        import tomllib
        pyproject = Path(__file__).resolve().parent.parent / "pyproject.toml"
        with open(pyproject, "rb") as f:
            data = tomllib.load(f)
        ver = data.get("project", {}).get("version")
        if ver:
            return ver
    except Exception:
        pass
    try:
        from importlib.metadata import version as _pkg_version
        return _pkg_version("vision-sidecar-mcp")
    except Exception:
        return "unknown"


SERVER_VERSION = _resolve_server_version()
TOOLS_AVAILABLE = [
    "analyze_image",
    "analyze_ui_screenshot",
    "extract_text_from_image",
    "extract_table",
    "analyze_structured",
    "diagnose_error",
    "check_vlm_status",
]


@mcp.tool()
def check_vlm_status() -> str:
    """Check if the VLM is available and responsive.

    Returns server config (version, URL, model, sampling profile, upscale threshold,
    tools_available list) plus the list of models the Ollama backend reports.
    """
    config_block = {
        "version": SERVER_VERSION,
        "tools_available": TOOLS_AVAILABLE,
        "ollama_url": OLLAMA_URL,
        "vlm_model": VLM_MODEL,
        "vlm_temperature": VLM_TEMPERATURE,
        "vlm_num_predict": VLM_NUM_PREDICT,
        "vlm_num_ctx": VLM_NUM_CTX,
        "vlm_top_p": VLM_TOP_P,
        "vlm_top_k": VLM_TOP_K,
        "vlm_repeat_penalty": VLM_REPEAT_PENALTY,
        "vlm_seed": VLM_SEED,
        "vlm_num_batch": VLM_NUM_BATCH,
        "vlm_num_keep": VLM_NUM_KEEP,
        "vlm_timeout_seconds": VLM_TIMEOUT,
        "vlm_prefill_thinking_close": VLM_PREFILL_THINKING_CLOSE,
        "upscale_below_width_px": UPSCALE_BELOW_WIDTH,
        "upscale_factor": UPSCALE_FACTOR,
        "max_image_dimension_px": MAX_IMAGE_DIMENSION,
    }

    if MOCK_MODE:
        return json.dumps({
            **config_block,
            "mock_mode": True,
            "status": "mock_ready",
            "note": "Set VISION_MOCK=0 to use real VLM",
        }, indent=2)

    log_call("status", "check_vlm_status", "BLOCK_PROBE_OLLAMA", phase="entry", url=OLLAMA_URL)
    try:
        with httpx.Client(timeout=10) as client:
            resp = client.get(f"{OLLAMA_URL}/api/tags")
            resp.raise_for_status()
            models = resp.json().get("models", [])

        model_names = [m.get("name", "") for m in models]
        vlm_available = any(VLM_MODEL in name for name in model_names)
        log_call(
            "status", "check_vlm_status", "BLOCK_PROBE_OLLAMA",
            phase="exit", status="ready" if vlm_available else "model_not_found",
            model_count=len(model_names), vlm_available=int(vlm_available),
        )

        return json.dumps({
            **config_block,
            "vlm_available": vlm_available,
            "available_models": model_names,
            "status": "ready" if vlm_available else "model_not_found",
        }, indent=2)
    except httpx.ConnectError:
        log_call("status", "check_vlm_status", "BLOCK_PROBE_OLLAMA", level=logging.WARNING, phase="exit", status="connection_failed")
        return json.dumps({
            **config_block,
            "status": "connection_failed",
            "error": "Cannot connect to Ollama server",
        }, indent=2)
    except Exception as e:
        return json.dumps({
            **config_block,
            "status": "error",
            "error": str(e),
        }, indent=2)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
