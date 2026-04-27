# Vision Sidecar — Quick Reference

## Purpose
Analyze images/screenshots via a VLM on Ollama exposed as MCP tools.

## Connection
- **Ollama URL:** configured via `OLLAMA_URL` env var (default: `http://localhost:11434`)
- **Model:** configured via `VLM_MODEL` env var (recommended: `qwen3-vl:8b` or any Ollama vision model)
- **Config:** `~/.config/kilo/kilo.jsonc` → `mcp.vision-sidecar`
- **Timeout:** 120 sec per request (configurable via `VLM_TIMEOUT`)

## Tools

### `analyze_image(image_path, prompt?)`
General image analysis. Returns structured markdown description.
```
Use: understand any visual content — screenshots, mockups, diagrams, photos.
Prompt: optional custom instruction. Default: general description.
```

### `analyze_ui_screenshot(image_path)`
Specialized UI/UX analysis. Returns component hierarchy, layout, colors, spacing.
```
Use: review landing pages, app screens, design mockups.
Returns: layout type, component tree, color scheme, spacing patterns, responsive hints.
```

### `extract_text_from_image(image_path)`
OCR — extracts all visible text preserving formatting.
```
Use: transcribe code screenshots, error messages, documents, tables.
Returns: plain text of everything visible in the image.
```

### `check_vlm_status()`
Health check. Returns connection status and model availability.
```
Use: verify Ollama is reachable before batch analysis.
```

## Typical Workflows

### 1. Review a live site
```bash
npx playwright screenshot --full-page https://example.com /tmp/shot.png
```
→ call `analyze_ui_screenshot("/tmp/shot.png")`
→ call `extract_text_from_image("/tmp/shot.png")` for copy-paste content

### 2. Analyze a Figma/design export
Save or screenshot the design → `analyze_image(path, "Compare this mockup with the current implementation: [describe differences]")`

### 3. Debug visual regression
Screenshot before & after → `analyze_image(path, "Describe any visual differences, layout shifts, or broken elements")`

### 4. Extract error from screenshot
`extract_text_from_image(path)` → get exact error text → paste into code search

## Tips
- Images up to **50MB** supported (PNG, JPEG, GIF, WebP)
- Use **absolute paths** for `image_path`
- Full-page screenshots (`--full-page`) give more context than viewport-only
- For complex pages, consider multiple viewport screenshots (desktop + mobile)
- VLM latency is ~30-60 sec; plan accordingly
- If VLM is unreachable, `check_vlm_status()` will show connection error
- Mock mode (`VISION_MOCK=1`) returns canned responses — useful for prompt development without VLM
