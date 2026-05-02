"""Local persistent telemetry for vision-sidecar-mcp.

Records one JSONL event per tool call to two locations (when applicable):

  <server-source>/.telemetry/                       — always (sidecar self-monitoring)
  <calling-project-root>/.vision-sidecar-telemetry/ — when image_path falls inside a git repo

`get_telemetry()` reads back the JSONL files and returns either an aggregate
snapshot (totals, by-tool breakdown, latency / response-char histograms with
p50/p95/p99) or the last N raw events.

GRACE module contract:
  PURPOSE: provide persistent, low-cardinality, JSON-only telemetry that
           survives MCP daemon restarts and accumulates across sessions
  SCOPE:   record_event() at tool exit; compute_snapshot() on demand;
           project-root detection; auto-gitignore on first project hit
  DEPENDS: stdlib only (json, datetime, pathlib, time, statistics, contextvars)
  ROLE:    UTILITY (cross-cutting observability)
"""

from __future__ import annotations

import contextvars
import functools
import json
import os
import statistics
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterator, TypeVar

# -- Env-driven config --------------------------------------------------------

_ENABLED = os.environ.get("VLM_TELEMETRY", "1") == "1"
_SERVER_DIR_OVERRIDE = os.environ.get("VLM_TELEMETRY_DIR")
# Default OFF — sidecar should not silently mutate user repos. Set to "1" to
# opt in to having `.vision-sidecar-telemetry/` appended to the project's
# .gitignore on first hit.
_AUTO_GITIGNORE = os.environ.get("VLM_TELEMETRY_AUTO_GITIGNORE", "0") == "1"
_PROJECT_DIR_NAME = ".vision-sidecar-telemetry"
_SERVER_DIR_NAME = ".telemetry"
_PROJECT_ROOT_MAX_WALK = 6  # how many ancestors of image_path to scan for .git
_HIST_RING_SIZE = 1000  # last-N samples per histogram metric

# Server source root = parent of the package directory
_SERVER_SOURCE_ROOT = Path(__file__).resolve().parent.parent

# In-flight event for the current tool call. Set by track_call() context manager;
# helper functions (_call_ollama, _encode_image, _try_parse_json) update fields via event_field().
_current_event: contextvars.ContextVar[dict[str, Any] | None] = contextvars.ContextVar(
    "current_event", default=None
)


# -- Public API ---------------------------------------------------------------

def is_enabled() -> bool:
    return _ENABLED


def server_dir() -> Path:
    """Resolve the server-side telemetry directory."""
    if _SERVER_DIR_OVERRIDE:
        return Path(_SERVER_DIR_OVERRIDE)
    return _SERVER_SOURCE_ROOT / _SERVER_DIR_NAME


def project_root_of(image_path: str | os.PathLike[str]) -> Path | None:
    """Walk up from image_path looking for .git. Returns the repo root, or None.

    Walks at most _PROJECT_ROOT_MAX_WALK ancestors so a stray image deep in /tmp
    doesn't accidentally find /Users/x/.git or similar.
    """
    try:
        p = Path(image_path).resolve()
    except Exception:
        return None
    candidates = [p, *p.parents][: _PROJECT_ROOT_MAX_WALK + 1]
    for ancestor in candidates:
        if (ancestor / ".git").exists():
            return ancestor
    return None


def project_dir(project_root: Path) -> Path:
    return project_root / _PROJECT_DIR_NAME


def event_field(**fields: Any) -> None:
    """Update the in-flight event from inside helper functions.

    No-op when telemetry is disabled or no track_call() context is active.
    """
    if not _ENABLED:
        return
    ev = _current_event.get()
    if ev is not None:
        ev.update(fields)


@contextmanager
def track_call(tool: str, *, image_path: str | None = None, **initial: Any):
    """Wrap a @mcp.tool() body to record a telemetry event on exit.

    Captures wall time, lets helper functions stash fields via event_field(),
    appends an exception summary on raise, and writes the event to JSONL on
    exit (success or failure).

    Args:
        tool: tool name (e.g. "analyze_structured")
        image_path: passed in by callers that take an image_path arg —
            used to detect the calling project root (when applicable).
        **initial: any other fields to stamp at start (viewport_hint, etc.)
    """
    if not _ENABLED:
        yield
        return

    ev: dict[str, Any] = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
        "tool": tool,
        **{k: v for k, v in initial.items() if v is not None or k == "viewport_hint"},
    }
    # Resolve project root early so it's recorded with the event (cheap ancestor walk).
    proj_root: Path | None = None
    if image_path:
        proj_root = project_root_of(image_path)
        if proj_root is not None:
            ev["project_root"] = str(proj_root)

    t0 = time.perf_counter()
    token = _current_event.set(ev)
    try:
        yield
    except Exception as e:
        ev.setdefault("error_type", type(e).__name__)
        ev.setdefault("error", str(e)[:200])
        raise
    finally:
        ev["total_wall_s"] = round(time.perf_counter() - t0, 3)
        _current_event.reset(token)
        try:
            _write_event(ev, proj_root)
        except Exception:
            # Telemetry must never break the call path. Swallow any IO error.
            pass


F = TypeVar("F", bound=Callable[..., Any])


def track(tool_name: str | None = None) -> Callable[[F], F]:
    """Decorator that wraps an MCP tool function with track_call().

    Auto-detects ``image_path`` (positional 0 or keyword) and ``viewport_hint``
    (keyword) on the wrapped function and forwards them to ``track_call``.

    Usage:
        @mcp.tool()
        @telemetry.track()
        def analyze_image(image_path, prompt=None, viewport_hint=None):
            ...

    No-op when telemetry is disabled. Preserves the wrapped function's
    signature via ``functools.wraps`` so FastMCP signature inspection still works.
    """

    def decorator(fn: F) -> F:
        name = tool_name or fn.__name__

        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            ip = kwargs.get("image_path")
            if ip is None and args and isinstance(args[0], str):
                ip = args[0]
            initial: dict[str, Any] = {}
            if "viewport_hint" in kwargs:
                initial["viewport_hint"] = kwargs.get("viewport_hint")
            if "error_context" in kwargs and kwargs["error_context"] is not None:
                initial["has_error_context"] = True
            with track_call(name, image_path=ip, **initial):
                return fn(*args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return decorator


# -- Internals ----------------------------------------------------------------

def _events_filename(now: datetime | None = None) -> str:
    d = (now or datetime.now(timezone.utc)).strftime("%Y-%m-%d")
    return f"events-{d}.jsonl"


def _ensure_dir(d: Path) -> None:
    d.mkdir(parents=True, exist_ok=True)


_GITIGNORE_MARKER = "# vision-sidecar-mcp local telemetry"
_GITIGNORE_LINE = f"{_PROJECT_DIR_NAME}/"


def _maybe_add_to_project_gitignore(project_root: Path) -> None:
    """Idempotently append the telemetry dir to the project's .gitignore."""
    gi = project_root / ".gitignore"
    try:
        existing = gi.read_text(encoding="utf-8") if gi.exists() else ""
        if _GITIGNORE_LINE in existing.splitlines():
            return
        suffix = "" if existing.endswith("\n") or not existing else "\n"
        with gi.open("a", encoding="utf-8") as f:
            f.write(f"{suffix}\n{_GITIGNORE_MARKER}\n{_GITIGNORE_LINE}\n")
    except Exception:
        # Don't disturb the caller's project on permission/IO failure.
        pass


def _write_event(ev: dict[str, Any], project_root: Path | None) -> None:
    line = json.dumps(ev, ensure_ascii=False) + "\n"
    fname = _events_filename()
    server_d = server_dir()
    _ensure_dir(server_d)
    with (server_d / fname).open("a", encoding="utf-8") as f:
        f.write(line)
    if project_root is not None:
        proj_d = project_dir(project_root)
        _ensure_dir(proj_d)
        if _AUTO_GITIGNORE:
            _maybe_add_to_project_gitignore(project_root)
        with (proj_d / fname).open("a", encoding="utf-8") as f:
            f.write(line)


# -- Snapshot computation -----------------------------------------------------

def _iter_events(directory: Path, *, limit: int | None = None) -> Iterator[dict[str, Any]]:
    """Yield events from all events-*.jsonl in directory, oldest day first.

    If limit is given, returns at most `limit` MOST RECENT events
    (ordered oldest-to-newest within the returned slice).
    """
    if not directory.exists():
        return
    files = sorted(directory.glob("events-*.jsonl"))
    if limit is None:
        for fp in files:
            with fp.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        yield json.loads(line)
                    except Exception:
                        continue
        return
    # Limit mode: read tail of files until we have `limit` events.
    collected: list[dict[str, Any]] = []
    for fp in reversed(files):
        with fp.open("r", encoding="utf-8") as f:
            day_events = []
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    day_events.append(json.loads(line))
                except Exception:
                    continue
        # Take from end of this day until we reach limit
        for ev in reversed(day_events):
            collected.append(ev)
            if len(collected) >= limit:
                break
        if len(collected) >= limit:
            break
    for ev in reversed(collected):
        yield ev


def _hist(values: list[float]) -> dict[str, Any]:
    if not values:
        return {"count": 0}
    sorted_vals = sorted(values)
    n = len(sorted_vals)

    def pct(p: float) -> float:
        if n == 1:
            return sorted_vals[0]
        idx = int(round((p / 100.0) * (n - 1)))
        return sorted_vals[max(0, min(n - 1, idx))]

    return {
        "count": n,
        "min": round(sorted_vals[0], 4),
        "max": round(sorted_vals[-1], 4),
        "sum": round(sum(sorted_vals), 4),
        "p50": round(pct(50), 4),
        "p95": round(pct(95), 4),
        "p99": round(pct(99), 4),
    }


def compute_snapshot(directory: Path) -> dict[str, Any]:
    """Read all events in `directory` and produce an aggregate snapshot.

    Histograms keep ALL samples (not ring-buffered) since we read from disk
    on demand; for typical sidecar volumes (~100/day) this stays cheap.
    """
    totals_by_tool: dict[str, int] = {}
    totals_by_status: dict[str, int] = {}
    parse_results: dict[str, int] = {}
    upscale_count = 0
    empty_response_count = 0
    error_count = 0
    first_ts: str | None = None
    last_ts: str | None = None
    total_calls = 0

    ollama_walls: list[float] = []
    total_walls: list[float] = []
    response_chars: list[int] = []
    image_bytes: list[int] = []

    for ev in _iter_events(directory):
        total_calls += 1
        ts = ev.get("ts")
        if ts:
            if first_ts is None or ts < first_ts:
                first_ts = ts
            if last_ts is None or ts > last_ts:
                last_ts = ts
        tool = ev.get("tool", "?")
        totals_by_tool[tool] = totals_by_tool.get(tool, 0) + 1
        st = ev.get("ollama_status") or ("error" if ev.get("error_type") else "n/a")
        totals_by_status[st] = totals_by_status.get(st, 0) + 1
        pr = ev.get("parse_result", "n/a")
        parse_results[pr] = parse_results.get(pr, 0) + 1
        if ev.get("upscaled"):
            upscale_count += 1
        if ev.get("response_chars") == 0 and ev.get("ollama_status") == "ok":
            empty_response_count += 1
        if ev.get("error_type"):
            error_count += 1

        if isinstance(ev.get("ollama_wall_s"), (int, float)):
            ollama_walls.append(float(ev["ollama_wall_s"]))
        if isinstance(ev.get("total_wall_s"), (int, float)):
            total_walls.append(float(ev["total_wall_s"]))
        if isinstance(ev.get("response_chars"), int):
            response_chars.append(ev["response_chars"])
        if isinstance(ev.get("image_bytes"), int):
            image_bytes.append(ev["image_bytes"])

    return {
        "computed_at": datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
        "directory": str(directory),
        "first_event_ts": first_ts,
        "last_event_ts": last_ts,
        "totals": {
            "calls": total_calls,
            "by_tool": dict(sorted(totals_by_tool.items(), key=lambda kv: -kv[1])),
            "by_status": totals_by_status,
            "parse": parse_results,
            "errors": error_count,
            "empty_responses": empty_response_count,
            "upscales": upscale_count,
        },
        "rates": {
            "upscale_rate": round(upscale_count / total_calls, 4) if total_calls else 0.0,
            "empty_response_rate": round(empty_response_count / total_calls, 4) if total_calls else 0.0,
            "error_rate": round(error_count / total_calls, 4) if total_calls else 0.0,
        },
        "ollama_wall_seconds": _hist(ollama_walls),
        "total_wall_seconds": _hist(total_walls),
        "response_chars": _hist([float(x) for x in response_chars]),
        "image_bytes": _hist([float(x) for x in image_bytes]),
    }


def recent_events(directory: Path, limit: int = 100) -> list[dict[str, Any]]:
    return list(_iter_events(directory, limit=limit))
