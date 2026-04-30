"""V-M-IMAGE — image preprocessing tests.

Asserts:
- Narrow images (width ≤ UPSCALE_BELOW_WIDTH) are upscaled by Lanczos
- Wide images are NOT upscaled
- _validate_image emits BLOCK_VALIDATE_IMAGE; _preprocess_image emits BLOCK_UPSCALE
- _encode_image emits BLOCK_ENCODE_IMAGE with image_sha256 and byte counts
"""

from __future__ import annotations

import io
from pathlib import Path

import pytest
from PIL import Image

from vision_sidecar.server import (
    _encode_image,
    _preprocess_image,
    _validate_image,
)


def _make_png_bytes(w: int, h: int, color: str = "white") -> bytes:
    im = Image.new("RGB", (w, h), color)
    buf = io.BytesIO()
    im.save(buf, format="PNG")
    return buf.getvalue()


# -- Upscale path --------------------------------------------------------------

def test_upscale_narrow_image_320_to_640():
    raw = _make_png_bytes(320, 568)
    processed, info = _preprocess_image(raw, "image/png")
    assert info["upscaled"] is True
    assert info["upscale_factor"] == 2
    assert info["final_size"] == [640, 1136]
    assert info["method"] == "Lanczos"
    # Output bytes should differ from input (resize was applied)
    assert processed != raw


def test_upscale_skipped_for_wide_image():
    raw = _make_png_bytes(800, 600)
    processed, info = _preprocess_image(raw, "image/png")
    assert "upscaled" not in info
    assert processed == raw  # unchanged passthrough


def test_upscale_emits_block_marker(captured_logs):
    _preprocess_image(_make_png_bytes(320, 568), "image/png")
    logs = captured_logs.getvalue()
    assert "BLOCK_UPSCALE" in logs
    assert "from_w=320" in logs
    assert "to_w=640" in logs
    assert "method=Lanczos" in logs


def test_upscale_does_not_emit_for_wide_image(captured_logs):
    _preprocess_image(_make_png_bytes(800, 600), "image/png")
    logs = captured_logs.getvalue()
    assert "BLOCK_UPSCALE" not in logs  # silent when no upscale


def test_upscale_robust_to_corrupt_input(captured_logs):
    # Invalid PNG data — preprocess should swallow and pass through
    processed, info = _preprocess_image(b"not a valid image", "image/png")
    assert info.get("preprocess_skipped") is True
    assert processed == b"not a valid image"
    logs = captured_logs.getvalue()
    assert "BLOCK_UPSCALE" in logs and "result=skipped" in logs


# -- Validate path -------------------------------------------------------------

def test_validate_image_emits_marker(tmp_path, captured_logs):
    img = tmp_path / "fixture.png"
    img.write_bytes(_make_png_bytes(100, 100))
    meta = _validate_image(str(img))
    assert meta["size_bytes"] > 0
    assert meta["mime"] == "image/png"
    logs = captured_logs.getvalue()
    assert "BLOCK_VALIDATE_IMAGE" in logs
    assert "size_bytes=" in logs


def test_validate_image_missing(tmp_path, captured_logs):
    with pytest.raises(FileNotFoundError):
        _validate_image(str(tmp_path / "does_not_exist.png"))
    logs = captured_logs.getvalue()
    assert "BLOCK_VALIDATE_IMAGE" in logs
    assert "result=not_found" in logs


# -- Encode path ---------------------------------------------------------------

def test_encode_image_emits_marker_with_sha(tmp_path, captured_logs):
    img = tmp_path / "fixture.png"
    img.write_bytes(_make_png_bytes(800, 600))
    b64, mime, info = _encode_image(str(img))
    assert mime == "image/png"
    assert len(b64) > 0
    logs = captured_logs.getvalue()
    assert "BLOCK_ENCODE_IMAGE" in logs
    assert "image_sha256=" in logs
    assert "raw_bytes=" in logs
    assert "b64_chars=" in logs


def test_encode_image_with_real_kombo_fixture(kombo_image, captured_logs):
    """End-to-end on a real fixture: validate + preprocess + encode."""
    b64, mime, info = _encode_image(str(kombo_image))
    assert mime in ("image/png", "image/jpeg", "image/webp")
    assert len(b64) > 1000  # real images produce non-trivial b64


def test_encode_small_image_triggers_upscale(small_kombo_image, captured_logs):
    """Real 320×568 fixture from the kombo dataset must trigger upscale path."""
    b64, mime, info = _encode_image(str(small_kombo_image))
    logs = captured_logs.getvalue()
    assert "BLOCK_UPSCALE" in logs
    # 10_small_mobile_stress.png is 320×568 → upscale to 640×1136
    assert "from_w=320" in logs and "to_w=640" in logs
