# Contributing

## Development Setup

```bash
git clone https://github.com/xronocode/vision-sidecar-mcp.git
cd vision-sidecar-mcp
uv sync
```

## Running Tests

```bash
# Mock mode test (no Ollama needed)
VISION_MOCK=1 uv run python3 -m vision_sidecar.server
```

## Making Changes

1. Create a feature branch
2. Make your changes
3. Test with `VISION_MOCK=1` first, then with a real VLM
4. Submit a pull request

## Code Style

- Follow PEP 8
- Use type hints
- No hardcoded URLs, IPs, or credentials
- Keep the server stateless

## Adding New Tools

1. Add a new function decorated with `@mcp.tool()` in `server.py`
2. Add mock response in mock mode
3. Update README.md and USAGE.md with the new tool
4. Test with both mock and real VLM
