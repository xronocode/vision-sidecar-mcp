"""Pytest configuration for vision-sidecar-mcp.

GRACE V-M-* evidence harness. Default to MOCK mode and INFO-level logging
so tests can assert against BLOCK markers without hitting Ollama.
"""

from __future__ import annotations

import io
import logging
import os
import sys
from pathlib import Path

import pytest

# Force MOCK before any vision_sidecar import so module-level constants pick up the right values.
os.environ.setdefault("VISION_MOCK", "1")
os.environ.setdefault("VLM_LOG_LEVEL", "INFO")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def captured_logs():
    """Capture vision_sidecar logger output. Yields the StringIO buffer.

    Usage:
        def test_block_emits(captured_logs):
            ... call something that should log ...
            assert "BLOCK_FOO" in captured_logs.getvalue()
    """
    from vision_sidecar import server

    buf = io.StringIO()
    handler = logging.StreamHandler(buf)
    handler.setFormatter(logging.Formatter("%(message)s"))

    original_handlers = list(server._logger.handlers)
    original_level = server._logger.level

    server._logger.handlers = [handler]
    server._logger.setLevel(logging.DEBUG)

    yield buf

    server._logger.handlers = original_handlers
    server._logger.setLevel(original_level)


@pytest.fixture
def kombo_image() -> Path:
    """Path to a known kombo eval fixture (used by tests that need a real PNG)."""
    p = PROJECT_ROOT / "eval_images" / "kombo" / "01_desktop_hero.png"
    if not p.exists():
        pytest.skip(f"missing fixture {p}")
    return p


@pytest.fixture
def small_kombo_image() -> Path:
    """320×568 small-mobile fixture — exercises the upscale path (V-M-IMAGE)."""
    p = PROJECT_ROOT / "eval_images" / "kombo" / "10_small_mobile_stress.png"
    if not p.exists():
        pytest.skip(f"missing fixture {p}")
    return p
