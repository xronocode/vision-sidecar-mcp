"""Cloud-fallback gate in run_vlm's auto mode.

auto mode must not upload images to z.ai silently: with VLM_ALLOW_CLOUD
unset, a busy GPU or an MLX error returns an error naming the opt-in;
with the opt-in set, the fallback fires. VLM_BACKEND=zai is an explicit
choice and is not gated.
"""

from unittest import mock

import pytest

from vision_sidecar import backends


def _run(**overrides):
    kwargs = dict(
        image_path="/tmp/x.png",
        image_b64="Zm9v",
        mime="image/png",
        prompt="describe",
        system_prompt="sys",
        num_predict=16,
        temperature=0.1,
    )
    kwargs.update(overrides)
    return backends.run_vlm(**kwargs)


def _patch_dispatch(monkeypatch, *, gpu_busy, mlx_result, zai_calls):
    monkeypatch.setattr(backends, "gpu_busy", lambda: gpu_busy)
    monkeypatch.setattr(backends, "call_mlx", lambda *a, **k: mlx_result)
    monkeypatch.setattr(
        backends, "call_zai", lambda *a, **k: zai_calls.append(1) or "cloud"
    )


def test_busy_gpu_without_optin_returns_error(monkeypatch):
    zai: list = []
    _patch_dispatch(monkeypatch, gpu_busy=(True, "whisper running"), mlx_result="", zai_calls=zai)
    monkeypatch.setattr(backends, "VLM_ALLOW_CLOUD", False)
    monkeypatch.setattr(backends, "VLM_BACKEND", "auto")
    content, meta = _run()
    assert content.startswith("[VLM_ERROR]")
    assert "VLM_ALLOW_CLOUD" in content
    assert zai == []
    assert meta["backend"] == "error"


def test_busy_gpu_with_optin_falls_back_to_cloud(monkeypatch):
    zai: list = []
    _patch_dispatch(monkeypatch, gpu_busy=(True, "whisper running"), mlx_result="", zai_calls=zai)
    monkeypatch.setattr(backends, "VLM_ALLOW_CLOUD", True)
    monkeypatch.setattr(backends, "VLM_BACKEND", "auto")
    content, meta = _run()
    assert content == "cloud"
    assert len(zai) == 1
    assert meta["backend"] == "zai" and meta["fallback_from"] == "mlx"


def test_mlx_error_without_optin_returns_error(monkeypatch):
    zai: list = []

    def boom(*a, **k):
        raise RuntimeError("mlx exploded")

    monkeypatch.setattr(backends, "gpu_busy", lambda: (False, ""))
    monkeypatch.setattr(backends, "call_mlx", boom)
    monkeypatch.setattr(
        backends, "call_zai", lambda *a, **k: zai_calls.append(1) or "cloud"
    )
    monkeypatch.setattr(backends, "VLM_ALLOW_CLOUD", False)
    monkeypatch.setattr(backends, "VLM_BACKEND", "auto")
    content, meta = _run()
    assert content.startswith("[VLM_ERROR]")
    assert "mlx exploded" in content and "VLM_ALLOW_CLOUD" in content
    assert zai == []
    assert meta["backend"] == "error"


def test_mlx_success_stays_local(monkeypatch):
    zai: list = []
    _patch_dispatch(monkeypatch, gpu_busy=(False, ""), mlx_result="local answer", zai_calls=zai)
    monkeypatch.setattr(backends, "VLM_ALLOW_CLOUD", False)
    monkeypatch.setattr(backends, "VLM_BACKEND", "auto")
    content, meta = _run()
    assert content == "local answer"
    assert zai == []
    assert meta["backend"] == "mlx"


def test_explicit_zai_backend_not_gated(monkeypatch):
    zai: list = []
    monkeypatch.setattr(
        backends, "call_zai", lambda *a, **k: zai.append(1) or "cloud"
    )
    monkeypatch.setattr(backends, "VLM_ALLOW_CLOUD", False)
    monkeypatch.setattr(backends, "VLM_BACKEND", "zai")
    content, meta = _run()
    assert content == "cloud"
    assert len(zai) == 1
    assert meta["backend"] == "zai"
