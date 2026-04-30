"""V-M-TOOLS-DIAG — diagnose_error tool tests (MOCK mode).

Per Phase-4 Step-4. The ui_diff sibling was dropped after VF-006 gate failed
(eval_results/smoke_multi_image/result.md), so M-TOOLS-DIAG admits only
diagnose_error.
"""

from __future__ import annotations

import json

from vision_sidecar import server


def test_diagnose_error_returns_envelope(kombo_image):
    out = server.diagnose_error(image_path=str(kombo_image))
    parsed = json.loads(out)
    assert "image" in parsed
    assert "model" in parsed
    assert "result" in parsed


def test_diagnose_error_mock_payload_shape(kombo_image):
    """Mock fixture must match the documented diagnosis schema."""
    out = server.diagnose_error(image_path=str(kombo_image))
    parsed = json.loads(out)
    diag = parsed["result"]
    assert diag["_mock"] is True
    # Required fields
    assert isinstance(diag["error_type"], str)
    assert isinstance(diag["description"], str)
    assert isinstance(diag["affected_elements"], list)
    assert "visible_error_text" in diag  # may be None
    assert isinstance(diag["suggested_fixes"], list)
    assert isinstance(diag["looks_correct"], bool)
    assert isinstance(diag["confidence"], dict)


def test_diagnose_error_passes_viewport_hint(kombo_image):
    out = server.diagnose_error(image_path=str(kombo_image), viewport_hint="small_mobile")
    parsed = json.loads(out)
    assert parsed["viewport_hint"] == "small_mobile"


def test_diagnose_error_passes_error_context(kombo_image):
    """error_context must round-trip into the response envelope."""
    ctx = "TypeError: Cannot read property 'foo' of undefined at line 42"
    out = server.diagnose_error(image_path=str(kombo_image), error_context=ctx)
    parsed = json.loads(out)
    assert parsed["error_context"] == ctx


def test_diagnose_error_dispatch_marker(kombo_image, captured_logs):
    server.diagnose_error(image_path=str(kombo_image), error_context="boom", viewport_hint="mobile")
    logs = captured_logs.getvalue()
    assert "BLOCK_DISPATCH_TOOL" in logs
    assert "tool_name=diagnose_error" in logs
    assert "has_error_context=1" in logs
    assert "viewport_hint=mobile" in logs


def test_diagnose_error_without_context_marker(kombo_image, captured_logs):
    server.diagnose_error(image_path=str(kombo_image))
    logs = captured_logs.getvalue()
    assert "tool_name=diagnose_error" in logs
    assert "has_error_context=0" in logs
