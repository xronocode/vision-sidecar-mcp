"""V-M-CONFIG — runtime config / env-var resolution tests.

These tests assert the *current* configuration after import. Because Python
caches modules, env-var changes after first import do not propagate. We
therefore validate the load-time defaults and document the contract.
"""

from __future__ import annotations

from vision_sidecar import server


def test_prefill_defaults_on():
    """Reasoning-leak workaround MUST default to enabled. See VF-002."""
    assert server.VLM_PREFILL_THINKING_CLOSE is True


def test_upscale_threshold_default():
    assert server.UPSCALE_BELOW_WIDTH == 400
    assert server.UPSCALE_FACTOR == 2


def test_sampling_profile_present():
    """V-M-OLLAMA scenario-3: full ML-team sampling profile resolved."""
    assert server.VLM_TEMPERATURE == 0.1
    assert server.VLM_NUM_PREDICT == 8192
    assert server.VLM_NUM_CTX == 32768
    assert server.VLM_TOP_P == 0.9
    assert server.VLM_TOP_K == 20
    assert server.VLM_REPEAT_PENALTY == 1.05
    assert server.VLM_NUM_BATCH == 1024
    assert server.VLM_NUM_KEEP == 0


def test_seed_default_42():
    assert server.VLM_SEED == 42


def test_mock_mode_active_in_test_env():
    """conftest.py sets VISION_MOCK=1 — server must pick it up."""
    assert server.MOCK_MODE is True


def test_log_level_resolution():
    """conftest.py sets VLM_LOG_LEVEL=INFO."""
    assert server.VLM_LOG_LEVEL == "INFO"
