"""V-M-OBSERVABILITY — log_call helper + dispatch markers.

Step-0 deliverable verification: confirms every @mcp.tool() emits
BLOCK_DISPATCH_TOOL with tool_name, and the log_call helper formats
output as `[VisionSidecar][module][fn][BLOCK]`.
"""

from __future__ import annotations

import json
import logging

from vision_sidecar import server
from vision_sidecar.server import log_call


def test_log_call_format(captured_logs):
    log_call("modX", "fnY", "BLOCK_Z", level=logging.INFO, foo="bar", n=3)
    logs = captured_logs.getvalue()
    assert "[VisionSidecar][modX][fnY][BLOCK_Z]" in logs
    assert "foo=bar" in logs
    assert "n=3" in logs


def test_log_call_respects_level(captured_logs):
    """At DEBUG level set by fixture, INFO must emit. WARNING also emits."""
    log_call("m", "f", "B1", level=logging.INFO)
    log_call("m", "f", "B2", level=logging.WARNING)
    logs = captured_logs.getvalue()
    assert "B1" in logs
    assert "B2" in logs


def test_log_call_no_kv_message(captured_logs):
    log_call("m", "f", "BLOCK_BARE")
    logs = captured_logs.getvalue()
    # Bare marker: no trailing kv
    assert "[VisionSidecar][m][f][BLOCK_BARE]" in logs


# -- Per-tool dispatch markers (mock mode) -------------------------------------

def test_analyze_image_dispatch_marker(kombo_image, captured_logs):
    server.analyze_image(image_path=str(kombo_image), viewport_hint="desktop")
    logs = captured_logs.getvalue()
    assert "BLOCK_DISPATCH_TOOL" in logs
    assert "tool_name=analyze_image" in logs
    assert "viewport_hint=desktop" in logs


def test_analyze_ui_screenshot_dispatch_marker(kombo_image, captured_logs):
    server.analyze_ui_screenshot(image_path=str(kombo_image))
    logs = captured_logs.getvalue()
    assert "tool_name=analyze_ui_screenshot" in logs


def test_extract_text_dispatch_marker(kombo_image, captured_logs):
    server.extract_text_from_image(image_path=str(kombo_image))
    logs = captured_logs.getvalue()
    assert "tool_name=extract_text_from_image" in logs


def test_extract_table_dispatch_marker(kombo_image, captured_logs):
    server.extract_table(image_path=str(kombo_image))
    logs = captured_logs.getvalue()
    assert "tool_name=extract_table" in logs


def test_analyze_structured_dispatch_marker(kombo_image, captured_logs):
    server.analyze_structured(image_path=str(kombo_image), viewport_hint="mobile")
    logs = captured_logs.getvalue()
    assert "tool_name=analyze_structured" in logs
    assert "viewport_hint=mobile" in logs


def test_check_vlm_status_emits_or_skips_probe(captured_logs):
    """In MOCK_MODE check_vlm_status returns mock without probing Ollama."""
    out = server.check_vlm_status()
    parsed = json.loads(out)
    assert parsed["mock_mode"] is True
    assert parsed["status"] == "mock_ready"
    # MOCK path does not emit BLOCK_PROBE_OLLAMA — that's expected
    logs = captured_logs.getvalue()
    assert "BLOCK_PROBE_OLLAMA" not in logs


def test_mock_analyze_structured_returns_valid_json(kombo_image):
    """Schema compliance smoke: mock fixture parses cleanly via _try_parse_json."""
    out = server.analyze_structured(image_path=str(kombo_image))
    parsed = json.loads(out)
    assert "result" in parsed
    assert parsed["result"]["_mock"] is True
