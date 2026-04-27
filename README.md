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

- **4 MCP tools** for different analysis modes (general, UI/UX, OCR, health check)
- **Mock mode** for development without a running VLM
- **Configurable** model, timeout, and Ollama URL via environment variables
- **50MB image limit** with format auto-detection (PNG, JPEG, GIF, WebP, BMP)
- **Zero external state** — pure proxy, no database, no caching

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

### `analyze_image(image_path, prompt?)`

General-purpose image analysis. Returns a structured markdown description.

```
image_path: Absolute path to the image file.
prompt:     Optional custom analysis prompt.
```

### `analyze_ui_screenshot(image_path)`

Specialized UI/UX analysis. Extracts component hierarchy, layout structure, color scheme, spacing patterns, and responsive design hints.

```
image_path: Absolute path to the UI screenshot.
```

### `extract_text_from_image(image_path)`

OCR-like text extraction. Transcribes all visible text preserving formatting, indentation, and structure.

```
image_path: Absolute path to the image.
```

### `check_vlm_status()`

Health check — verifies Ollama connectivity and model availability.

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

## Architecture

```
vision-sidecar-mcp/
├── pyproject.toml           # Dependencies and entry point
├── README.md                # This file
├── USAGE.md                 # Detailed workflows and tips
├── LICENSE                  # MIT
└── vision_sidecar/
    ├── __init__.py
    └── server.py            # FastMCP server with 4 tools
```

## License

[MIT](./LICENSE)
