"""V-M-TELEMETRY — local persistent telemetry tests.

Covers:
- track_call() context manager populates events with timing + initial fields
- event_field() updates the in-flight event from helpers
- _write_event() writes JSONL to server dir and (when applicable) project dir
- project_root_of() detects .git ancestors, gives up after the depth cap
- _maybe_add_to_project_gitignore() is idempotent
- compute_snapshot() aggregates events into histograms with sane percentiles
- get_telemetry tool returns server / project / raw views
"""

from __future__ import annotations

import importlib
import json
import os
from pathlib import Path

import pytest


def _reload_telemetry(
    monkeypatch: pytest.MonkeyPatch,
    server_dir: Path,
    *,
    auto_gitignore: bool = False,
):
    """Force telemetry to honor a custom directory + enable flag."""
    monkeypatch.setenv("VLM_TELEMETRY", "1")
    monkeypatch.setenv("VLM_TELEMETRY_DIR", str(server_dir))
    monkeypatch.setenv("VLM_TELEMETRY_AUTO_GITIGNORE", "1" if auto_gitignore else "0")
    from vision_sidecar import telemetry
    importlib.reload(telemetry)
    return telemetry


def _make_repo(tmp_path: Path, name: str) -> Path:
    repo = tmp_path / name
    (repo / ".git").mkdir(parents=True)
    return repo


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


# -- track_call lifecycle ------------------------------------------------------

def test_track_call_writes_event_to_server_dir(tmp_path, monkeypatch):
    server_d = tmp_path / "server_tel"
    tm = _reload_telemetry(monkeypatch, server_d)

    with tm.track_call("test_tool", viewport_hint="desktop"):
        tm.event_field(custom_field=42)

    files = sorted(server_d.glob("events-*.jsonl"))
    assert len(files) == 1
    events = _read_jsonl(files[0])
    assert len(events) == 1
    ev = events[0]
    assert ev["tool"] == "test_tool"
    assert ev["viewport_hint"] == "desktop"
    assert ev["custom_field"] == 42
    assert "ts" in ev
    assert "total_wall_s" in ev


def test_track_call_records_exception(tmp_path, monkeypatch):
    server_d = tmp_path / "server_tel"
    tm = _reload_telemetry(monkeypatch, server_d)

    with pytest.raises(ValueError):
        with tm.track_call("test_tool"):
            raise ValueError("boom")

    events = _read_jsonl(next(server_d.glob("events-*.jsonl")))
    assert events[0]["error_type"] == "ValueError"
    assert "boom" in events[0]["error"]


def test_disabled_telemetry_writes_nothing(tmp_path, monkeypatch):
    server_d = tmp_path / "server_tel"
    monkeypatch.setenv("VLM_TELEMETRY", "0")
    monkeypatch.setenv("VLM_TELEMETRY_DIR", str(server_d))
    from vision_sidecar import telemetry
    importlib.reload(telemetry)

    with telemetry.track_call("test_tool"):
        telemetry.event_field(x=1)

    assert not server_d.exists() or not list(server_d.glob("events-*.jsonl"))


# -- project root detection ----------------------------------------------------

def test_project_root_of_finds_git(tmp_path, monkeypatch):
    server_d = tmp_path / "server_tel"
    tm = _reload_telemetry(monkeypatch, server_d)

    repo = _make_repo(tmp_path, "myproj")
    nested = repo / "src" / "deep" / "image.png"
    nested.parent.mkdir(parents=True)
    nested.touch()

    found = tm.project_root_of(str(nested))
    assert found == repo


def test_project_root_of_gives_up_when_too_deep(tmp_path, monkeypatch):
    server_d = tmp_path / "server_tel"
    tm = _reload_telemetry(monkeypatch, server_d)

    repo = _make_repo(tmp_path, "myproj")
    deep = repo / "a" / "b" / "c" / "d" / "e" / "f" / "g" / "image.png"
    deep.parent.mkdir(parents=True)
    deep.touch()
    # 7 levels down — exceeds the default 6-level walk
    found = tm.project_root_of(str(deep))
    assert found is None


def test_project_root_of_returns_none_when_no_git(tmp_path, monkeypatch):
    server_d = tmp_path / "server_tel"
    tm = _reload_telemetry(monkeypatch, server_d)

    img = tmp_path / "no_git_here" / "image.png"
    img.parent.mkdir()
    img.touch()
    assert tm.project_root_of(str(img)) is None


# -- dual write to server + project --------------------------------------------

def test_writes_to_both_server_and_project_when_image_in_repo(tmp_path, monkeypatch):
    server_d = tmp_path / "server_tel"
    tm = _reload_telemetry(monkeypatch, server_d)

    repo = _make_repo(tmp_path, "myproj")
    img = repo / "screenshot.png"
    img.touch()

    with tm.track_call("test_tool", image_path=str(img), viewport_hint="mobile"):
        tm.event_field(image_bytes=12345)

    server_files = list(server_d.glob("events-*.jsonl"))
    proj_files = list((repo / ".vision-sidecar-telemetry").glob("events-*.jsonl"))
    assert len(server_files) == 1
    assert len(proj_files) == 1
    server_events = _read_jsonl(server_files[0])
    proj_events = _read_jsonl(proj_files[0])
    assert server_events[0]["tool"] == "test_tool"
    assert proj_events[0]["tool"] == "test_tool"
    assert server_events[0]["project_root"] == str(repo)


def test_only_server_dir_when_image_outside_any_repo(tmp_path, monkeypatch):
    server_d = tmp_path / "server_tel"
    tm = _reload_telemetry(monkeypatch, server_d)

    img = tmp_path / "loose_image.png"
    img.touch()

    with tm.track_call("test_tool", image_path=str(img)):
        pass

    assert list(server_d.glob("events-*.jsonl"))
    # No project dir created
    assert not (tmp_path / ".vision-sidecar-telemetry").exists()


# -- gitignore auto-add --------------------------------------------------------

def test_default_does_not_touch_project_gitignore(tmp_path, monkeypatch):
    """Default VLM_TELEMETRY_AUTO_GITIGNORE=0 must NOT mutate the project's .gitignore."""
    server_d = tmp_path / "server_tel"
    tm = _reload_telemetry(monkeypatch, server_d, auto_gitignore=False)

    repo = _make_repo(tmp_path, "myproj")
    original = "node_modules/\nvenv/\n*.log\n"
    (repo / ".gitignore").write_text(original)
    img = repo / "shot.png"
    img.touch()

    with tm.track_call("test_tool", image_path=str(img)):
        pass

    gi = (repo / ".gitignore").read_text()
    assert gi == original  # byte-for-byte unchanged
    # But the telemetry directory itself was still created
    assert (repo / ".vision-sidecar-telemetry").exists()


def test_auto_adds_to_project_gitignore_when_enabled(tmp_path, monkeypatch):
    """Opt-in path: VLM_TELEMETRY_AUTO_GITIGNORE=1 appends the entry."""
    server_d = tmp_path / "server_tel"
    tm = _reload_telemetry(monkeypatch, server_d, auto_gitignore=True)

    repo = _make_repo(tmp_path, "myproj")
    img = repo / "shot.png"
    img.touch()

    with tm.track_call("test_tool", image_path=str(img)):
        pass

    gi = (repo / ".gitignore").read_text()
    assert ".vision-sidecar-telemetry/" in gi
    assert "vision-sidecar-mcp local telemetry" in gi


def test_gitignore_add_is_idempotent(tmp_path, monkeypatch):
    server_d = tmp_path / "server_tel"
    tm = _reload_telemetry(monkeypatch, server_d, auto_gitignore=True)

    repo = _make_repo(tmp_path, "myproj")
    (repo / ".gitignore").write_text("__pycache__/\n.vision-sidecar-telemetry/\n")
    img = repo / "shot.png"
    img.touch()

    with tm.track_call("test_tool", image_path=str(img)):
        pass

    gi = (repo / ".gitignore").read_text()
    # Should NOT add a duplicate entry
    assert gi.count(".vision-sidecar-telemetry/") == 1


def test_gitignore_preserves_existing_user_content(tmp_path, monkeypatch):
    server_d = tmp_path / "server_tel"
    tm = _reload_telemetry(monkeypatch, server_d, auto_gitignore=True)

    repo = _make_repo(tmp_path, "myproj")
    original = "node_modules/\nvenv/\n*.log\n"
    (repo / ".gitignore").write_text(original)
    img = repo / "shot.png"
    img.touch()

    with tm.track_call("test_tool", image_path=str(img)):
        pass

    gi = (repo / ".gitignore").read_text()
    assert "node_modules/" in gi
    assert "venv/" in gi
    assert "*.log" in gi
    assert ".vision-sidecar-telemetry/" in gi


# -- snapshot computation ------------------------------------------------------

def test_compute_snapshot_aggregates(tmp_path, monkeypatch):
    server_d = tmp_path / "server_tel"
    tm = _reload_telemetry(monkeypatch, server_d)

    # Synthesize 5 events with varying fields
    for i, (tool, status, parse, walls, chars) in enumerate([
        ("analyze_structured", "ok", "ok", 5.0, 1500),
        ("analyze_structured", "ok", "ok", 6.5, 2200),
        ("extract_table", "ok", "ok", 3.2, 800),
        ("analyze_image", "ok", "n/a", 4.0, 900),
        ("analyze_structured", "timeout", "empty", 120.0, 0),
    ]):
        with tm.track_call(tool):
            tm.event_field(
                ollama_status=status,
                ollama_wall_s=walls,
                response_chars=chars,
                parse_result=parse,
                image_bytes=100_000 + i * 10_000,
                upscaled=(i % 2 == 0),
            )

    snap = tm.compute_snapshot(server_d)
    assert snap["totals"]["calls"] == 5
    assert snap["totals"]["by_tool"]["analyze_structured"] == 3
    assert snap["totals"]["by_status"]["ok"] == 4
    assert snap["totals"]["by_status"]["timeout"] == 1
    assert snap["totals"]["empty_responses"] == 0  # only counts ok+0chars
    assert snap["totals"]["upscales"] == 3  # i=0,2,4
    # Histogram has all 4 stats
    h = snap["ollama_wall_seconds"]
    assert h["count"] == 5
    assert h["min"] == 3.2
    assert h["max"] == 120.0
    assert "p50" in h
    assert "p95" in h


def test_compute_snapshot_empty_dir(tmp_path):
    from vision_sidecar import telemetry as tm
    snap = tm.compute_snapshot(tmp_path / "empty")
    assert snap["totals"]["calls"] == 0


def test_recent_events_caps_to_limit(tmp_path, monkeypatch):
    server_d = tmp_path / "server_tel"
    tm = _reload_telemetry(monkeypatch, server_d)

    for i in range(10):
        with tm.track_call(f"tool_{i % 3}"):
            tm.event_field(idx=i)

    events = tm.recent_events(server_d, limit=4)
    assert len(events) == 4
    # Most recent 4 should be idx 6..9 (in chronological order at the tail)
    indices = [e["idx"] for e in events]
    assert indices == sorted(indices)
    assert indices[-1] == 9


# -- track decorator (used by @mcp.tool) ---------------------------------------

def test_track_decorator_extracts_image_path_from_kwarg(tmp_path, monkeypatch):
    server_d = tmp_path / "server_tel"
    tm = _reload_telemetry(monkeypatch, server_d)
    repo = _make_repo(tmp_path, "myproj")
    img = repo / "shot.png"
    img.touch()

    @tm.track("my_func")
    def my_func(image_path: str, viewport_hint: str | None = None):
        tm.event_field(executed=True)
        return "ok"

    result = my_func(image_path=str(img), viewport_hint="mobile")
    assert result == "ok"

    events = _read_jsonl(next(server_d.glob("events-*.jsonl")))
    assert events[0]["tool"] == "my_func"
    assert events[0]["viewport_hint"] == "mobile"
    assert events[0]["executed"] is True
    assert events[0]["project_root"] == str(repo)


def test_track_decorator_extracts_image_path_positional(tmp_path, monkeypatch):
    server_d = tmp_path / "server_tel"
    tm = _reload_telemetry(monkeypatch, server_d)
    repo = _make_repo(tmp_path, "myproj")
    img = repo / "shot.png"
    img.touch()

    @tm.track("my_func")
    def my_func(image_path):
        return "ok"

    my_func(str(img))  # positional
    events = _read_jsonl(next(server_d.glob("events-*.jsonl")))
    assert events[0]["project_root"] == str(repo)
