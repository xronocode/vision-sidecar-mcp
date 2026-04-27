import base64
import json
import mimetypes
import os
from datetime import datetime, timezone
from pathlib import Path

import httpx
from mcp.server.fastmcp import FastMCP

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
VLM_MODEL = os.environ.get("VLM_MODEL", "minicpm-v")
VLM_TIMEOUT = float(os.environ.get("VLM_TIMEOUT", "120"))
MOCK_MODE = os.environ.get("VISION_MOCK", "1") == "1"

SYSTEM_PROMPT = (
    "You are a UI/UX analysis assistant. "
    "Describe the image in structured markdown. "
    "For UI screenshots: list components, layout, colors, text content. "
    "For code screenshots: transcribe the code exactly. "
    "For diagrams: describe the structure and relationships. "
    "Be precise and detailed. Respond in English."
)

mcp = FastMCP("vision-sidecar", instructions="Vision analysis tools using a local VLM via Ollama")


MOCK_ANALYSIS = """## Image Analysis (MOCK)

**Layout:** Centered card layout with vertical stacking.

**Components detected:**
- Header bar with navigation links (Home, About, Contact)
- Hero section with heading "Welcome to Our Platform"
- CTA button "Get Started" (blue, rounded corners)
- Two-column feature cards section below
- Footer with copyright text

**Color scheme:**
- Background: white (#FFFFFF)
- Primary: blue (#3B82F6)
- Text: dark gray (#1F2937)
- Accent: green (#10B981)

**Typography:** Sans-serif, 16px base, headings bold.
**Spacing:** 24px padding on cards, 32px gaps between sections.

> MOCK response. Set VISION_MOCK=0 to use the real VLM.
"""

MOCK_UI_ANALYSIS = """## UI Component Analysis (MOCK)

### Layout Structure
- Type: Flexbox column layout
- Max-width: 1200px, centered
- Breakpoints: likely 768px, 1024px

### Component Tree
```
├── Navbar
│   ├── Logo
│   └── NavLinks (3 items)
├── Hero
│   ├── Heading (h1)
│   ├── Subheading (p)
│   └── Button (CTA)
├── Features (grid 2-col)
│   ├── Card 1 (icon + title + text)
│   └── Card 2 (icon + title + text)
└── Footer
    └── Copyright
```

### Styling Notes
- Cards: shadow-md, rounded-lg, p-6
- Button: bg-blue-500, text-white, px-4, py-2, rounded
- Responsive: cards stack on mobile

> MOCK response. Set VISION_MOCK=0 to use the real VLM.
"""

MOCK_OCR_TEXT = """function handleSubmit(event) {
  event.preventDefault();
  const formData = new FormData(event.target);
  const data = Object.fromEntries(formData.entries());
  console.log("Form submitted:", data);
  fetch("/api/submit", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  })
    .then(res => res.json())
    .then(result => console.log("Success:", result))
    .catch(err => console.error("Error:", err));
}

> MOCK response. Set VISION_MOCK=0 to use the real VLM.
"""


def _validate_image(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Image not found: {path}")
    if p.stat().st_size > 50 * 1024 * 1024:
        raise ValueError(f"Image too large: {p.stat().st_size / 1024 / 1024:.1f}MB (max 50MB)")

    mime, _ = mimetypes.guess_type(str(p))
    if not mime or not mime.startswith("image/"):
        mime = "image/png"

    return {
        "path": str(p),
        "size_bytes": p.stat().st_size,
        "size_mb": round(p.stat().st_size / 1024 / 1024, 2),
        "mime": mime,
        "modified": datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc).isoformat(),
    }


def _encode_image(path: str) -> tuple[str, str]:
    p = Path(path)
    mime, _ = mimetypes.guess_type(str(p))
    if not mime or not mime.startswith("image/"):
        mime = "image/png"

    with open(p, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")

    return b64, mime


def _call_ollama(image_b64: str, prompt: str) -> str:
    payload = {
        "model": VLM_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt, "images": [image_b64]},
        ],
        "stream": False,
        "options": {"temperature": 0.3, "num_predict": 2048},
    }

    with httpx.Client(timeout=VLM_TIMEOUT) as client:
        resp = client.post(f"{OLLAMA_URL}/api/chat", json=payload)
        resp.raise_for_status()
        data = resp.json()

    return data.get("message", {}).get("content", "")


@mcp.tool()
def analyze_image(image_path: str, prompt: str | None = None) -> str:
    """Analyze an image using a local vision-language model.

    Sends the image to Ollama VLM and returns a structured text description.
    Use this when you need to understand screenshots, UI mockups, diagrams,
    or any visual content.

    Args:
        image_path: Absolute path to the image file (PNG, JPEG, GIF, WebP, etc.)
        prompt: Optional custom prompt for analysis. Defaults to general description.

    Returns:
        Structured text description of the image content.
    """
    meta = _validate_image(image_path)

    if MOCK_MODE:
        return json.dumps({
            "image": meta,
            "model": f"{VLM_MODEL} (MOCK)",
            "prompt": prompt or "default",
            "analysis": MOCK_ANALYSIS,
        }, ensure_ascii=False, indent=2)

    image_b64, _ = _encode_image(image_path)
    result = _call_ollama(image_b64, prompt or "Describe this image in detail. If it's a UI screenshot, describe layout, components, text, and styling.")

    return json.dumps({"image": meta, "model": VLM_MODEL, "analysis": result}, ensure_ascii=False, indent=2)


@mcp.tool()
def analyze_ui_screenshot(image_path: str) -> str:
    """Analyze a UI screenshot and extract component hierarchy.

    Specialized tool for UI/UX screenshots that focuses on extracting
    component structure, layout information, and styling details
    relevant for frontend development.

    Args:
        image_path: Absolute path to the UI screenshot.

    Returns:
        JSON with component hierarchy and layout details.
    """
    meta = _validate_image(image_path)

    if MOCK_MODE:
        return json.dumps({
            "image": meta,
            "model": f"{VLM_MODEL} (MOCK)",
            "ui_analysis": MOCK_UI_ANALYSIS,
        }, ensure_ascii=False, indent=2)

    prompt = (
        "Analyze this UI screenshot and provide:\n"
        "1. Overall layout structure (grid, flex, etc.)\n"
        "2. All visible components (buttons, inputs, cards, etc.)\n"
        "3. Text content with approximate positions\n"
        "4. Color scheme (background, primary, secondary, accent)\n"
        "5. Spacing and alignment patterns\n"
        "6. Responsive design hints\n"
        "Format as structured markdown."
    )

    image_b64, _ = _encode_image(image_path)
    result = _call_ollama(image_b64, prompt)

    return json.dumps({"image": meta, "model": VLM_MODEL, "ui_analysis": result}, ensure_ascii=False, indent=2)


@mcp.tool()
def extract_text_from_image(image_path: str) -> str:
    """Extract text content from an image (OCR-like functionality).

    Uses the vision model to transcribe all visible text in the image.
    Useful for screenshots of code, documents, or error messages.

    Args:
        image_path: Absolute path to the image.

    Returns:
        Extracted text content.
    """
    meta = _validate_image(image_path)

    if MOCK_MODE:
        return json.dumps({
            "image": meta,
            "model": f"{VLM_MODEL} (MOCK)",
            "extracted_text": MOCK_OCR_TEXT,
        }, ensure_ascii=False, indent=2)

    prompt = (
        "Transcribe ALL text visible in this image exactly as written. "
        "Preserve formatting, indentation, and structure. "
        "If this is code, preserve the exact syntax. "
        "Output only the transcribed text, nothing else."
    )

    image_b64, _ = _encode_image(image_path)
    result = _call_ollama(image_b64, prompt)

    return json.dumps({"image": meta, "model": VLM_MODEL, "extracted_text": result}, ensure_ascii=False, indent=2)


@mcp.tool()
def check_vlm_status() -> str:
    """Check if the VLM (Vision Language Model) is available and responsive.

    Returns status information about the Ollama server and the vision model.
    """
    if MOCK_MODE:
        return json.dumps({
            "ollama_url": OLLAMA_URL,
            "vlm_model": VLM_MODEL,
            "mock_mode": True,
            "status": "mock_ready",
            "note": "Set VISION_MOCK=0 to use real VLM",
        }, indent=2)

    try:
        with httpx.Client(timeout=10) as client:
            resp = client.get(f"{OLLAMA_URL}/api/tags")
            resp.raise_for_status()
            models = resp.json().get("models", [])

        model_names = [m.get("name", "") for m in models]
        vlm_available = any(VLM_MODEL in name for name in model_names)

        return json.dumps({
            "ollama_url": OLLAMA_URL,
            "vlm_model": VLM_MODEL,
            "vlm_available": vlm_available,
            "available_models": model_names,
            "status": "ready" if vlm_available else "model_not_found",
        }, indent=2)
    except httpx.ConnectError:
        return json.dumps({
            "ollama_url": OLLAMA_URL,
            "status": "connection_failed",
            "error": "Cannot connect to Ollama server",
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "ollama_url": OLLAMA_URL,
            "status": "error",
            "error": str(e),
        }, indent=2)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
