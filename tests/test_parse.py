"""V-M-PARSE — tolerance JSON parser tests.

Asserts deterministic behavior of `_try_parse_json`:
- never raises
- handles fenced code blocks
- handles surrounding chatter
- emits BLOCK_PARSE_JSON marker via log_call
"""

from __future__ import annotations

from vision_sidecar.server import _try_parse_json


def test_direct_json():
    obj, err = _try_parse_json('{"a": 1}')
    assert obj == {"a": 1}
    assert err is None


def test_fenced_json():
    obj, err = _try_parse_json('```json\n{"a": 1}\n```')
    assert obj == {"a": 1}
    assert err is None


def test_fenced_json_no_lang():
    obj, err = _try_parse_json('```\n{"a": 1}\n```')
    assert obj == {"a": 1}
    assert err is None


def test_chatter_around_json():
    """Brace-fallback path: model wraps JSON with explanatory prose."""
    raw = "Sure, here is the JSON you asked for:\n{\"key\": \"value\"}\nLet me know if you need more."
    obj, err = _try_parse_json(raw)
    assert obj == {"key": "value"}
    assert err is None


def test_empty_response():
    obj, err = _try_parse_json("")
    assert obj is None
    assert err == "empty response"


def test_garbage_response():
    obj, err = _try_parse_json("absolutely not json")
    assert obj is None
    assert err is not None and "json parse error" in err


def test_never_raises_on_truncated():
    # Truncated JSON should return parse_error, not raise
    obj, err = _try_parse_json('{"a": 1, "b": 2')  # missing closing brace
    assert obj is None
    assert err is not None


def test_emits_block_marker(captured_logs):
    _try_parse_json('{"x": 42}')
    logs = captured_logs.getvalue()
    assert "BLOCK_PARSE_JSON" in logs
    assert "result=ok" in logs
    assert "path=direct" in logs


def test_emits_brace_fallback_marker(captured_logs):
    _try_parse_json("prose {\"x\": 42} more prose")
    logs = captured_logs.getvalue()
    assert "BLOCK_PARSE_JSON" in logs
    assert "path=brace_fallback" in logs


def test_emits_empty_marker(captured_logs):
    _try_parse_json("")
    logs = captured_logs.getvalue()
    assert "BLOCK_PARSE_JSON" in logs
    assert "result=empty_response" in logs
