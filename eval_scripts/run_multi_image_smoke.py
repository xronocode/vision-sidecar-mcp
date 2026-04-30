"""Multi-image smoke test for qwen3-vl:8b — VF-006 gating gate.

Sends 3 before/after image pairs from the kombo eval dataset to Ollama
/api/chat with `images=[b64_before, b64_after]` in a single user message,
then saves raw responses for manual rubric scoring.

This script is the Step-1 deliverable of Phase-4 (v0.3.0): its result
determines whether `ui_diff` ships in v0.3.0 or is dropped.

Decision matrix (per docs/verification-plan.xml VF-006):
  0/3 pairs satisfy rubric  → ui_diff DROPPED from v0.3.0
  1/3 pairs satisfy rubric  → conditional ship with explicit limitations doc
  2-3/3 pairs satisfy        → ship

Rubric:
  r-1: model output references BOTH images explicitly ("image 1" / "image 2")
       — no conflation
  r-2: ≥ 2 of 3 expected-detection bullets per pair appear in output
       (substring or near-paraphrase)
  r-3: no fabricated elements not present in either image

Usage:
  OLLAMA_URL=http://INTERNAL-HOST:11434 VLM_MODEL=qwen3-vl:8b \\
    python eval_scripts/run_multi_image_smoke.py

Outputs (under eval_results/smoke_multi_image/):
  pair_<N>_<mode>.json — full request/response snapshot per pair
  summary.json         — aggregate {pair_id, mode, response_chars, wall_seconds, status}
  (then) result.md     — human rubric scoring + final decision (written manually)
"""

from __future__ import annotations

import base64
import json
import os
import sys
import time
from pathlib import Path

import httpx

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
VLM_MODEL = os.environ.get("VLM_MODEL", "qwen3-vl:8b")
VLM_TIMEOUT = float(os.environ.get("VLM_TIMEOUT", "240"))
VLM_NUM_PREDICT = int(os.environ.get("VLM_NUM_PREDICT", "8192"))
VLM_NUM_CTX = int(os.environ.get("VLM_NUM_CTX", "32768"))
VLM_TEMPERATURE = float(os.environ.get("VLM_TEMPERATURE", "0.1"))
VLM_SEED_RAW = os.environ.get("VLM_SEED", "42").strip()
VLM_SEED: int | None = int(VLM_SEED_RAW) if VLM_SEED_RAW else None

PROJECT_ROOT = Path(__file__).resolve().parent.parent
IMAGE_DIR = PROJECT_ROOT / "eval_images" / "kombo"
OUTPUT_DIR = PROJECT_ROOT / "eval_results" / "smoke_multi_image"

# VF-006 fixture pairs (from docs/verification-plan.xml)
PAIRS: list[dict] = [
    {
        "pair_id": 1,
        "label": "responsive_break",
        "before": "01_desktop_hero.png",
        "after": "07_mobile_hero.png",
        "expected_detection": [
            "same hero content",
            "h1 wraps to multiple lines on mobile (4 lines)",
            "egg illustration removed on mobile",
            "ctas reflow to 2 rows on mobile",
        ],
    },
    {
        "pair_id": 2,
        "label": "extreme_break",
        "before": "01_desktop_hero.png",
        "after": "10_small_mobile_stress.png",
        "expected_detection": [
            "same hero, drastically narrower viewport",
            "h1 wraps to 5 lines",
            "ctas below the fold (clipped)",
            "subhead truncated",
        ],
    },
    {
        "pair_id": 3,
        "label": "stack_responsive",
        "before": "02_desktop_audience_sections.png",
        "after": "08_mobile_audience_sections.png",
        "expected_detection": [
            "same three audience cards stacked",
            "teacher waitlist link visible in desktop, clipped on mobile",
            "how it works step grid present in desktop, absent in mobile",
        ],
    },
]

PROMPT = (
    "You are looking at TWO screenshots provided in order: IMAGE 1 (before) "
    "and IMAGE 2 (after). They show the same web page rendered at different "
    "viewport widths.\n\n"
    "Report:\n"
    "1. CHANGES — concrete visible differences. Reference each change as "
    "\"in IMAGE 1 ... but in IMAGE 2 ...\". Be specific about elements, "
    "positions, and text wrap.\n"
    "2. UNCHANGED — key elements that look the same in both.\n"
    "3. CLIPPING — whether either image shows content clipped at the bottom "
    "edge (cut-off CTAs, partial paragraphs).\n\n"
    "Rules:\n"
    "- Always reference both IMAGE 1 and IMAGE 2 explicitly. Do not blend them.\n"
    "- Do not invent elements that are not visible.\n"
    "- Preserve glyphs verbatim (✦ stays ✦, → stays →).\n"
    "- Be concise and structured."
)


def encode_image(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def call_ollama_two_images(
    b64_a: str,
    b64_b: str,
    *,
    suppress_thinking: bool,
) -> dict:
    """Send a single user message with TWO images. Returns request+response snapshot."""
    messages = [
        {
            "role": "user",
            "content": PROMPT,
            "images": [b64_a, b64_b],
        }
    ]
    if suppress_thinking:
        messages.append({"role": "assistant", "content": "</think>\n\n"})

    options = {
        "temperature": VLM_TEMPERATURE,
        "num_predict": VLM_NUM_PREDICT,
        "num_ctx": VLM_NUM_CTX,
        "top_p": 0.9,
        "top_k": 20,
        "repeat_penalty": 1.05,
        "num_batch": 1024,
        "num_keep": 0,
    }
    if VLM_SEED is not None:
        options["seed"] = VLM_SEED

    payload = {
        "model": VLM_MODEL,
        "messages": messages,
        "stream": False,
        "options": options,
    }

    t0 = time.perf_counter()
    try:
        with httpx.Client(timeout=VLM_TIMEOUT) as client:
            resp = client.post(f"{OLLAMA_URL}/api/chat", json=payload)
            resp.raise_for_status()
            data = resp.json()
        wall = round(time.perf_counter() - t0, 2)
        content = data.get("message", {}).get("content", "")
        return {
            "ok": True,
            "wall_seconds": wall,
            "response_chars": len(content),
            "response": content,
            "messages_array_shape": [
                {"role": m["role"], "content_chars": len(m.get("content", "")), "image_count": len(m.get("images", []))}
                for m in messages
            ],
            "options": options,
        }
    except Exception as e:
        return {
            "ok": False,
            "wall_seconds": round(time.perf_counter() - t0, 2),
            "error_type": type(e).__name__,
            "error": str(e)[:400],
        }


def main() -> int:
    print(f"OLLAMA_URL = {OLLAMA_URL}")
    print(f"VLM_MODEL  = {VLM_MODEL}")
    print(f"OUTPUT_DIR = {OUTPUT_DIR}")
    print()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    summary: list[dict] = []

    # Default: SUPPRESS_THINKING=False (diff needs reasoning, per VF-006 design notes).
    # If results are poor, retry with prefill — but start as-designed.
    mode = os.environ.get("SMOKE_MODE", "no_prefill")
    suppress_thinking = mode == "with_prefill"

    for pair in PAIRS:
        before_path = IMAGE_DIR / pair["before"]
        after_path = IMAGE_DIR / pair["after"]
        if not before_path.exists() or not after_path.exists():
            print(f"SKIP pair {pair['pair_id']}: missing fixtures")
            continue

        print(f"--- pair {pair['pair_id']} ({pair['label']}) [{mode}] ---")
        print(f"    before: {before_path.name}  ({before_path.stat().st_size} bytes)")
        print(f"    after:  {after_path.name}   ({after_path.stat().st_size} bytes)")

        b64_a = encode_image(before_path)
        b64_b = encode_image(after_path)

        result = call_ollama_two_images(b64_a, b64_b, suppress_thinking=suppress_thinking)

        snapshot = {
            "pair_id": pair["pair_id"],
            "label": pair["label"],
            "mode": mode,
            "before": pair["before"],
            "after": pair["after"],
            "expected_detection": pair["expected_detection"],
            **result,
        }
        out_file = OUTPUT_DIR / f"pair_{pair['pair_id']}_{mode}.json"
        out_file.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2))

        if result.get("ok"):
            print(f"    ok={result['ok']}  wall={result['wall_seconds']}s  "
                  f"response_chars={result['response_chars']}")
        else:
            print(f"    FAILED: {result.get('error_type')}: {result.get('error')}")

        summary.append({
            "pair_id": pair["pair_id"],
            "label": pair["label"],
            "mode": mode,
            "ok": result.get("ok"),
            "wall_seconds": result.get("wall_seconds"),
            "response_chars": result.get("response_chars", 0),
        })
        print()

    summary_file = OUTPUT_DIR / f"summary_{mode}.json"
    summary_file.write_text(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"Wrote {len(summary)} snapshots + summary to {OUTPUT_DIR}")
    print()
    print("Next: open each pair_*.json and score against the rubric")
    print("      (r-1 explicit refs, r-2 ≥2/3 detections, r-3 no fabrications),")
    print(f"      then write {OUTPUT_DIR}/result.md with the final decision.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
