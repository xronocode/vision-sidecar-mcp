# Vision Sidecar MCP

An MCP (Model Context Protocol) server that gives AI agents the ability to **see** — analyze screenshots, UI mockups, diagrams, and any visual content through a local VLM (Vision Language Model) running on [Ollama](https://ollama.com).

Designed for [Kilo Code](https://kilo.ai), but works with any MCP-compatible client.

## How It Works

```
┌──────────────┐     stdio/MCP      ┌──────────────────┐     HTTP      ┌─────────┐
│  AI Agent    │ ◄──────────────── │  vision-sidecar  │ ────────────► │  Ollama │
│  (Kilo/etc.) │                    │  (this server)   │    /api/chat  │  + VLM  │
└──────────────┘                    └──────────────────┘               └─────────┘
```

1. Agent captures a screenshot (e.g. via Playwright) or receives an image path
2. Calls one of the MCP tools (`analyze_image`, `analyze_ui_screenshot`, `extract_text_from_image`)
3. Server base64-encodes the image, sends it to Ollama VLM
4. VLM returns structured text analysis → back to the agent

## Features

- **8 MCP tools**: `analyze_image`, `analyze_ui_screenshot`, `extract_text_from_image`, `extract_table`, `analyze_structured`, `diagnose_error`, `get_telemetry`, `check_vlm_status`
- **Hardened extraction-only system prompt** — forbids hex-code invention, requires per-element color attribution, preserves icon glyphs (✦, →) verbatim, flags below-fold clipping
- **`viewport_hint` parameter** (`desktop`/`tablet`/`mobile`/`small_mobile`) — viewport-aware analysis with explicit clipping checks for narrow viewports
- **Auto-upscale** for narrow screenshots (≤400px wide) using Pillow Lanczos 2× — improves OCR on tight mobile layouts
- **Structured JSON output** via `analyze_structured` — schema with `glyphs_and_icons`, `below_fold_or_clipped`, per-block color descriptors, and a fenced `interpretation` block
- **Error / broken-UI diagnosis** via `diagnose_error` — returns structured JSON with `error_type`, `affected_elements`, `suggested_fixes`; optional `error_context` for cross-referencing console/log output
- **Structured logging** with 7 GRACE BLOCK markers (`BLOCK_VALIDATE_IMAGE`, `BLOCK_UPSCALE`, `BLOCK_ENCODE_IMAGE`, `BLOCK_CALL_OLLAMA`, `BLOCK_PARSE_JSON`, `BLOCK_PROBE_OLLAMA`, `BLOCK_DISPATCH_TOOL`) — opt-in via `VLM_LOG_LEVEL=INFO`
- **Persistent local telemetry** (default ON) — every tool call written as JSONL to `<server>/.telemetry/` and (when image_path is inside a git repo) also to `<repo>/.vision-sidecar-telemetry/`. Aggregate snapshots with p50/p95/p99 latency and per-tool / per-status breakdown via the `get_telemetry` tool. Survives MCP daemon restarts. Disable via `VLM_TELEMETRY=0`
- **44 module-level tests** in `tests/` (no Ollama required) — `pytest tests/` runs in ~0.5s
- **Mock mode** for development without a running VLM
- **Configurable** model, temperature, timeout, num_predict, upscale threshold via environment variables
- **50MB image limit** with format auto-detection (PNG, JPEG, GIF, WebP, BMP)
- **Zero external state** — pure proxy, no database, no caching

> **Note on `ui_diff`:** v0.3.0 deliberately does NOT ship a multi-image comparison tool. A gating smoke test ([`eval_results/smoke_multi_image/result.md`](eval_results/smoke_multi_image/result.md)) showed that qwen3-vl:8b fabricates cross-image elements (claims a desktop-only egg illustration is "partially clipped" in mobile shots where it's hidden by responsive rules) on 0/3 fixture pairs. Use two `analyze_structured` calls and diff the JSONs downstream instead.

## Requirements

- Python ≥ 3.11
- [uv](https://docs.astral.sh/uv/) package manager
- [Ollama](https://ollama.com) with a vision model installed (e.g. `qwen3-vl`, `llava`, `minicpm-v`)
- [Playwright](https://playwright.dev/) (optional, for capturing screenshots)

## Installation

### Clone

```bash
git clone https://github.com/xronocode/vision-sidecar-mcp.git
cd vision-sidecar-mcp
uv sync
```

### Verify Ollama

```bash
# Check that Ollama is running and has a vision model
curl http://localhost:11434/api/tags | python3 -c \
  "import sys,json; print([m['name'] for m in json.load(sys.stdin)['models']])"
```

If you don't have a vision model yet:

```bash
ollama pull qwen3-vl:8b
```

### Configure Kilo Code

Add to `~/.config/kilo/kilo.jsonc` in the `"mcp"` section:

```jsonc
"vision-sidecar": {
  "type": "local",
  "command": [
    "uv",
    "run",
    "--project",
    "/path/to/vision-sidecar-mcp",
    "python3",
    "-m",
    "vision_sidecar.server"
  ],
  "enabled": true,
  "timeout": 120000,
  "environment": {
    "OLLAMA_URL": "http://localhost:11434",
    "VLM_MODEL": "qwen3-vl:8b",
    "VLM_TIMEOUT": "120",
    "VISION_MOCK": "0"
  }
}
```

For remote Ollama instances, change `OLLAMA_URL` to the server address.

### Other MCP Clients

This server uses the standard MCP stdio transport. To run it directly:

```bash
OLLAMA_URL=http://localhost:11434 VLM_MODEL=qwen3-vl:8b uv run python3 -m vision_sidecar.server
```

Refer to your MCP client's documentation for registering local MCP servers.

## Tools

### `analyze_image(image_path, prompt?, viewport_hint?)`

General-purpose image analysis. Returns markdown description under the hardened extraction system prompt.

```
image_path:    Absolute path to the image file.
prompt:        Optional custom analysis prompt.
viewport_hint: Optional one of "desktop" | "tablet" | "mobile" | "small_mobile".
```

### `analyze_ui_screenshot(image_path, viewport_hint?)`

Specialized UI/UX analysis. Extracts component hierarchy, layout, qualitative color descriptors, glyph callouts, and clipping flags.

### `extract_text_from_image(image_path)`

OCR-like text extraction. Transcribes all visible text preserving formatting and icon glyphs verbatim.

### `extract_table(image_path)`

Dedicated table-extraction tool. Returns parsed JSON `{ present, row_count, col_count, header_row, rows }`. Includes the row-label column when present (top-left cell as `""`).

### `analyze_structured(image_path, viewport_hint?)`

Returns a structured JSON analysis with:
- `image_type`, `viewport_class` (closed enums)
- `visible_text[]` with per-block role/x_position/color_descriptor/weight
- `key_ui_elements[]`, `layout_structure`, `buttons_and_links[]`
- `numbers_dates_amounts[]`, `table_content`, `glyphs_and_icons[]`
- `uncertain_items[]`, `below_fold_or_clipped` (clipping detection)
- Optional `interpretation` block (fenced from observation fields)
- `confidence` (overall/ocr/color/layout)

### `diagnose_error(image_path, error_context?, viewport_hint?)`

Analyzes a screenshot showing a broken UI / error / clipping issue and proposes actionable fixes. Returns the same parse-tolerant JSON envelope as `analyze_structured` / `extract_table` (`result` holds the parsed diagnosis, or `raw` + `parse_error` if the model output didn't parse).

```
image_path:    Absolute path to the screenshot.
error_context: Optional console/terminal/log text. When provided, it is appended
               to the user prompt as a fenced block so the model cross-references
               console output with what's visible.
viewport_hint: Optional viewport class.
```

Diagnosis schema: `error_type` (enum: `layout_break`/`missing_element`/`overflow`/`clipping`/`error_message`/`crash`/`404`/`console_error`/`validation_error`/`z_index`/`other`), `description`, `affected_elements[]` (with `location`), `visible_error_text` (verbatim if present, else `null`), `suggested_fixes[]` (2–3 concrete CSS/HTML/responsive recommendations), `looks_correct` (bool — `true` only if no error visible), `confidence`.

Sample real-call output is captured in [`eval_results/diagnose_error_smoke/`](eval_results/diagnose_error_smoke/).

### `get_telemetry(project_path?, raw?, raw_limit?)`

Returns a snapshot of persistent local telemetry — counters, per-tool breakdown, latency / response / image-size histograms with p50/p95/p99.

```
project_path: Optional path inside a git repo. When given, returns the
              per-project snapshot from <repo-root>/.vision-sidecar-telemetry/
              instead of the server-global snapshot.
raw:          If true, returns the most recent `raw_limit` events as a list
              instead of the aggregate.
raw_limit:    Cap on raw events (default 100, max 5000).
```

Snapshot schema includes:
- `totals` — `calls`, `by_tool`, `by_status`, `parse`, `errors`, `empty_responses`, `upscales`
- `rates` — `upscale_rate`, `empty_response_rate`, `error_rate`
- `ollama_wall_seconds`, `total_wall_seconds`, `response_chars`, `image_bytes` — each with `{ count, min, max, sum, p50, p95, p99 }`

Telemetry is enabled by default. Set `VLM_TELEMETRY=0` to disable.

### `check_vlm_status()`

Health check — verifies Ollama connectivity and reports server config (`version`, `tools_available`, URL, model, full sampling profile, prefill flag, upscale threshold) plus the list of models the Ollama backend reports.

## Usage Examples

### Screenshot + UI analysis

```bash
npx playwright screenshot --full-page https://example.com /tmp/shot.png
```

Then call `analyze_ui_screenshot("/tmp/shot.png")` to get layout, components, and colors.

### Extract error text

`extract_text_from_image("/tmp/error.png")` — get exact error text for code search.

### Compare mockup vs implementation

`analyze_image("/tmp/mockup.png", "Compare this design with the current implementation. List differences.")`

### Mock mode

Set `VISION_MOCK=1` to get canned responses without calling Ollama. Useful for developing prompts or testing MCP integration.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_URL` | `http://localhost:11434` | Ollama API URL |
| `VLM_MODEL` | `minicpm-v` | Vision model name in Ollama |
| `VLM_TIMEOUT` | `120` | Request timeout in seconds |
| `VLM_TEMPERATURE` | `0.1` | Sampling temperature (lower = more deterministic extraction) |
| `VLM_NUM_PREDICT` | `8192` | Max output tokens (raised to fit dense schema responses) |
| `VLM_NUM_CTX` | `32768` | Context window. Default 2048-4096 in Ollama is too small for image + schema + system prompt |
| `VLM_TOP_P` | `0.9` | Nucleus sampling cutoff |
| `VLM_TOP_K` | `20` | Top-k sampling cutoff |
| `VLM_REPEAT_PENALTY` | `1.05` | Penalty applied to repeated tokens |
| `VLM_SEED` | `42` | Pin random seed for reproducible outputs (set empty to use random) |
| `VLM_NUM_BATCH` | `1024` | Tokens processed per batch on the GPU during prompt eval |
| `VLM_NUM_KEEP` | `0` | Number of tokens to keep from the previous request (0 = clean state per request) |
| `VLM_PREFILL_THINKING_CLOSE` | `1` | Append assistant turn with `</think>\n\n` so reasoning VLMs (qwen3-vl, etc.) skip thinking and emit response directly. Set `0` only for non-reasoning models. **Required for multi-image too** — without it, two-image calls also return empty content |
| `VLM_LOG_LEVEL` | `WARNING` | Logger level for `vision_sidecar` (Python `logging` standard names). Set to `INFO` to surface BLOCK markers (`[VisionSidecar][module][fn][BLOCK_NAME] k=v`) — useful for tracing tool dispatch, ollama calls, parse fallbacks. `DEBUG` adds full preprocess + sampling dumps |
| `VLM_TELEMETRY` | `1` | Persistent local telemetry. `1` = on (default), `0` = off |
| `VLM_TELEMETRY_DIR` | `<server>/.telemetry` | Override the server-side telemetry directory. Per-project directory (`<repo>/.vision-sidecar-telemetry/`) is always inferred from `image_path` and not configurable |
| `VISION_UPSCALE_BELOW_WIDTH` | `400` | Auto-upscale images whose width is ≤ this (px) |
| `VISION_UPSCALE_FACTOR` | `2` | Upscale multiplier when triggered (Lanczos resampling) |
| `VISION_MOCK` | `1` | `1` = mock responses, `0` = real VLM calls |

## Recommended Models

| Model | Size | Notes |
|-------|------|-------|
| `qwen3-vl:8b` | ~6GB | Best balance of speed and quality |
| `llava:7b` | ~4.7GB | Good general-purpose VLM |
| `minicpm-v` | ~5.5GB | Fast, decent quality |

All models require an Ollama server with sufficient RAM/VRAM.

## Limitations

- Max image size: 50MB
- VLM latency: ~30-60 seconds per request (depends on model and hardware)
- Text output quality depends on the VLM model — larger models produce better analysis
- No streaming — full response is returned after VLM completes

## Development

```bash
uv sync --extra dev      # install pytest
pytest tests/            # 44 module-level checks, no Ollama required, ~0.5s
```

`tests/` contains deterministic mock-mode checks for the JSON parser, Lanczos upscale, env-var resolution, log markers, and tool dispatch. Run before any pull request.

## Architecture

```
vision-sidecar-mcp/
├── pyproject.toml                           # Dependencies and entry point
├── README.md                                # This file
├── USAGE.md                                 # Detailed workflows and tips
├── LICENSE                                  # MIT
├── vision_sidecar/
│   ├── __init__.py
│   └── server.py                            # FastMCP server with 7 tools
├── tests/                                   # pytest mock-mode checks
│   ├── conftest.py
│   ├── test_parse.py
│   ├── test_image.py
│   ├── test_config.py
│   ├── test_logging.py
│   └── test_diagnose.py
├── eval_scripts/
│   └── run_multi_image_smoke.py             # VF-006 gating runner
├── eval_images/kombo/                       # 10-shot eval dataset
└── eval_results/
    ├── kombo/                               # cycle-1 baseline
    ├── kombo_after_tuning/                  # cycle-2 (v0.2.2)
    ├── opus_groundtruth/                    # frontier ground truth
    ├── zai/                                 # cloud GLM 4-way comparison
    ├── smoke_multi_image/                   # ui_diff gate decision
    ├── diagnose_error_smoke/                # diagnose_error real-call evidence
    └── v030_release_evidence.md             # v0.3.0 ship checklist
```

## Evaluation

The `eval_results/` tree records a multi-stack comparison on a 10-screenshot dataset captured from a real marketing site (`eval_images/kombo/`). `eval_results/zai/aggregate_4way_comparison.md` summarizes the four columns:

- **Opus 4.7** (frontier ceiling) — composite **5.0**
- **local-tuned (v0.2.2/v0.3.0)** — composite **4.1** (~82% of frontier)
- **zai cloud (GLM)** — composite **3.9** (~78% of frontier)
- **local-baseline (pre-tuning)** — composite **3.1** (~62% of frontier)

The tuned local model slightly outperforms the GLM-backed cloud VLM on aggregate. Residual gap to frontier sits in three known places: subtle color discrimination (e.g. distinguishing a deliberately greyed eyebrow from a purple one), exact wrap-line counting on mobile H1s, and design-intent inference. v0.3.0 is purely additive to v0.2.2 and does not change these numbers — see [`eval_results/v030_release_evidence.md`](eval_results/v030_release_evidence.md) for the no-regression rationale.

## License

[MIT](./LICENSE)
