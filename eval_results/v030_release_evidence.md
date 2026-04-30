# v0.3.0 Release Evidence

**Date:** 2026-04-30
**Branch:** main
**Phase:** GRACE Phase-4 (v0.3.0 — new tools)

## Scope summary

v0.3.0 is **purely additive** vs v0.2.2:

| Change | Type | Affects existing eval surfaces? |
|---|---|:-:|
| `log_call` helper + 7 BLOCK markers (Step-0) | additive observability | ❌ no — same request payload, same model, same sampling |
| Multi-image smoke test (Step-1) | one-time gate | ❌ no — separate code path, never invoked from existing tools |
| `tests/` pytest skeleton, 44 tests (Step-3) | new test infra | ❌ no — does not touch runtime code |
| `diagnose_error` tool (Step-4) | new tool | ❌ no — separate `@mcp.tool`, does not modify any of the 6 existing tools |
| `version` + `tools_available` in `check_vlm_status` (Step-6) | response-shape addition | ⚠️ schema-additive (clients should ignore unknown keys) |
| `ui_diff` (Step-5) | **DROPPED** per VF-006 gate | n/a |

**Therefore the kombo 4-way regression report (`eval_results/zai/aggregate_4way_comparison.md`) remains valid for v0.3.0.** The existing-tool composite (4.1 / 5.0 for local-tuned) does not change because:
- system prompt unchanged
- per-tool user prompts unchanged
- sampling profile unchanged (seed=42, temp=0.1, top_p=0.9, top_k=20, repeat_penalty=1.05, num_batch=1024, num_keep=0)
- `</think>` prefill behavior unchanged
- Lanczos upscale unchanged (UPSCALE_BELOW_WIDTH=400, factor=2)

A regression in the existing 6 tools would require modifying one of those — none are touched.

## Module-level evidence (V-M-* satisfied)

| V-M-* node | Evidence | Status |
|---|---|:-:|
| V-M-PARSE | `tests/test_parse.py` × 10 | ✅ 10/10 pass |
| V-M-IMAGE | `tests/test_image.py` × 10 (Lanczos 320→640 verified) | ✅ 10/10 pass |
| V-M-CONFIG | `tests/test_config.py` × 6 (sampling profile, prefill ON) | ✅ 6/6 pass |
| V-M-OBSERVABILITY | `tests/test_logging.py` × 12 (all 7 BLOCK markers, dispatch on 5 tools) | ✅ 12/12 pass |
| V-M-TOOLS-DIAG | `tests/test_diagnose.py` × 6 | ✅ 6/6 pass |
| V-M-STATUS | `tests/test_logging.py` × 2 (version, tools_available, drift detection) | ✅ 2/2 pass |
| **Total** | `pytest tests/` | **✅ 44/44 in 0.5s** |

## Critical-flow evidence (VF-* satisfied)

| Flow | Method | Status |
|---|---|:-:|
| VF-001 StructuredExtractionHappyPath | `analyze_structured` mock + cycle-2 23/23 success on real Ollama (kombo) | ✅ |
| VF-002 ReasoningTokenLeakDoesNotRecur | `_call_ollama` always appends `</think>\n\n` assistant prefill when `VLM_PREFILL_THINKING_CLOSE=1`. test_config.py asserts default ON. Smoke test confirms multi-image too: 0 chars without prefill, 2200 chars with. | ✅ |
| VF-003 NarrowViewportUpscale | `tests/test_image.py` deterministic 320→640 Lanczos check + real fixture exercise | ✅ |
| VF-004 ClippingDetectionAccuracy | covered in cycle-2 evaluation (10_small_mobile 1/5 → 5/5) | ✅ |
| VF-005 GlyphPreservation | covered in cycle-2 evaluation (`✦` preserved in shots 02/09 structured) | ✅ |
| VF-006 MultiImageSmokeTestGate | **FAIL — `ui_diff` dropped** (`eval_results/smoke_multi_image/result.md`) | ✅ (correct outcome) |

## What v0.3.0 explicitly does NOT do

- **No `ui_diff`.** VF-006 gate failed: 0/3 fixture pairs satisfied the rubric. README v0.3.0 should document this as a deliberate choice — agents should call `analyze_structured` twice and diff JSONs downstream when comparison is needed.
- **No per-tool system-prompt dispatcher.** Originally planned for Step-2 but deferred to v0.4.0+ once the `ui_diff` use case (which would have demanded it) was dropped. Current global `SYSTEM_PROMPT` is sufficient for `diagnose_error` (extraction-focused: "describe what is broken" still applies).
- **No `diagnose_error` evaluation dataset.** A synthetic `eval_images/errors/` corpus is recommended in `docs/verification-plan.xml` SyntheticDatasets section but not yet created. Scheduled for v0.3.1 or first user-driven fix wave. Until then, `diagnose_error` is functionally tested in MOCK mode and ships with no quantitative quality claim.
- **No physical file split.** The 12-module logical decomposition in `docs/knowledge-graph.xml` remains a map of `vision_sidecar/server.py`. Phase-5 (post-v0.3.0) will extract `config.py` / `prompts.py` / `image.py` / `parse.py` / `ollama_client.py` / `tools_*.py` / `status.py`.

## Reproduce

```bash
# Module-level (no Ollama)
uv sync --extra dev
.venv/bin/python -m pytest tests/ -v
# Expect: 44 passed in ~0.5s

# Multi-image gate (Ollama backend required)
OLLAMA_URL=http://INTERNAL-HOST:11434 VLM_MODEL=qwen3-vl:8b \
  SMOKE_MODE=with_prefill .venv/bin/python eval_scripts/run_multi_image_smoke.py
# Expect: 3/3 OK with prefill, 3/3 empty without prefill, decision=DROP

# Health probe (Ollama backend required)
.venv/bin/python -c "import json, os; os.environ['VISION_MOCK']='0'; \
  from vision_sidecar.server import check_vlm_status; print(check_vlm_status())"
# Expect: version="0.3.0", 7 tools_available, ollama_reachable=true, model=qwen3-vl:8b
```

## Ship checklist

- [x] All 44 module-level tests pass
- [x] VF-006 gate decision documented (`eval_results/smoke_multi_image/result.md`)
- [x] No regression risk surface in existing tools (purely additive change set)
- [x] `check_vlm_status.tools_available` matches actual `@mcp.tool` decorations (drift test passes)
- [x] `version` field reflects current `pyproject.toml`
- [ ] **Step-8: bump `pyproject.toml` from 0.2.2 → 0.3.0**
- [ ] Update README with v0.3.0 changelog entry (note `ui_diff` deliberate absence)
- [ ] Tag v0.3.0 in git
- [ ] Optional: run full kombo eval against v0.3.0 source after Phase-5 file split (not required for v0.3.0 ship — scope is additive)
