# Multi-Image Smoke Test — VF-006 Gate Decision

**Date:** 2026-04-30
**Model:** qwen3-vl:8b via Ollama (INTERNAL-HOST:11434)
**Sampling:** ML-team profile (seed=42, temp=0.1, top_p=0.9, top_k=20, repeat_penalty=1.05)
**Prompt:** `eval_scripts/run_multi_image_smoke.py` PROMPT (structured before/after comparison, explicit IMAGE 1 / IMAGE 2 references)
**Snapshots:** `pair_{1,2,3}_{no_prefill,with_prefill}.json`

## TL;DR — DECISION: ❌ DROP `ui_diff` from v0.3.0

Out of 3 fixture pairs, **0/3 satisfied the full rubric** (r-1 ✓ + r-2 + r-3). The model can correctly *reference* two images by index (r-1 passes 3/3), but it **fabricates elements** present in only one image (r-3 fails 3/3) and **misses or contradicts the most important visual changes** (r-2 fails 2/3).

Shipping `ui_diff` would deliver a tool that produces confident, well-structured, **wrong** comparisons — strictly worse than instructing agents to call `analyze_structured` twice and compare the JSONs themselves.

---

## Critical methodology finding

The original VF-006 hypothesis assumed `suppress_thinking=False` would help diff reasoning. **It does the opposite.**

| Mode | Pairs OK | Avg response_chars | Avg wall_seconds |
|---|---:|---:|---:|
| `no_prefill` (suppress_thinking=False) | 3/3 HTTP-200 | **0** | 137s |
| `with_prefill` (suppress_thinking=True) | 3/3 HTTP-200 | **2210** | 5.4s |

Without `</think>` prefill the model fills `num_predict=8192` with `<think>` tokens just like in single-image extraction — only worse, because two visual contexts amplify reasoning. **Prefill is required for multi-image too.** The verification-plan's hint that diff "needs reasoning" was wrong.

---

## Rubric scoring

| Pair | r-1 (refs both) | r-2 (≥2/3 expected) | r-3 (no fabrications) | Verdict |
|---|:-:|:-:|:-:|:-:|
| 1: desktop_hero ↔ mobile_hero | ✅ | ⚠️ ~1/4 | ❌ | **FAIL** |
| 2: desktop_hero ↔ small_mobile_stress | ✅ | ❌ 0/4 | ❌ | **FAIL** |
| 3: desktop_audience ↔ mobile_audience | ✅ | ⚠️ 1/3 | ❌ | **FAIL** |

### Pair 1 — desktop_hero (1440×900) vs mobile_hero (390×844)
- ✅ r-1: refs IMAGE 1 / IMAGE 2 throughout
- ⚠️ r-2: misses the H1 wrap-line change (talks about "description paragraph" wrap instead); CTA reflow noted but described as "compact vertical stack" rather than 2-row reflow; egg removal not detected
- ❌ r-3: **claims "purple oval is partially clipped at the top edge" in IMAGE 2** — the egg is entirely absent in mobile (responsive rule). Also claims FOR PARENTS header is present in both — IMAGE 2 only shows the top of FOR KIDS

### Pair 2 — desktop_hero (1440×900) vs small_mobile_stress (320×568)
- ✅ r-1: refs IMAGE 1 / IMAGE 2 throughout
- ❌ r-2: **inverted the H1 wrap claim** — says "the headline is fully visible without wrapping (all text on one line) in IMAGE 2", actual is wraps to 5 lines; CTAs claimed "partially visible at bottom" but actual is entirely below fold; subhead truncation missed entirely
- ❌ r-3: same purple-oval fabrication ("partially cropped off the right edge in IMAGE 2"); claims FOR KIDS / FOR PARENTS sections "entirely cut off" in IMAGE 2 — these sections don't appear at all in 320×568 hero shot

### Pair 3 — desktop_audience vs mobile_audience
- ✅ r-1: refs IMAGE 1 / IMAGE 2 throughout
- ⚠️ r-2: catches FOR TEACHERS body truncation in IMAGE 2 (✓); misses 3-card stacking similarity; misses HOW IT WORKS step-grid absence
- ❌ r-3: **directly contradicts ground truth** — "Join the teacher waitlist → are fully visible and identical in both images" (in IMAGE 2 this link is below the fold, not visible); claims "HOW IT WORKS section partially visible (text cut off at top edge) in IMAGE 2" — HOW IT WORKS is not in IMAGE 2 at all

---

## Failure pattern (cross-pair)

The model exhibits **inference-from-priors instead of pixel-grounding**:
- Sees a desktop hero (IMAGE 1) with a purple egg, then "knows" the page has an egg, and reports the egg as "partially visible / clipped" in the mobile counterpart even though it's gone.
- Recalls the page structure (FOR KIDS / FOR PARENTS / FOR TEACHERS / HOW IT WORKS) and **describes elements as present in IMAGE 2 that are simply not in the frame**.
- Confuses "below fold" with "partially visible" when content is fully out of frame.

This is a class of error frontier models also occasionally make, but at 8B parameter count it is dominant. The signal-to-noise ratio is too low for production use.

---

## Decision (per VF-006 matrix)

**0/3 pairs satisfy the full rubric → `ui_diff` is DROPPED from v0.3.0.**

### Implications for v0.3.0 scope

- ✅ `diagnose_error` ships independently (single-image, lower failure surface)
- ❌ `ui_diff` does **not** ship in v0.3.0
- 📝 README v0.3.0 should explicitly mention "ui_diff intentionally not provided — local 8B VLMs hallucinate cross-image presence; use two `analyze_structured` calls + JSON diff downstream instead"
- 📝 If a future release adopts a larger model (e.g. Qwen3-VL 32B), re-run this exact smoke test before re-enabling `ui_diff`

### Implications for `docs/verification-plan.xml`

1. **Correct DF-UI-DIFF guidance**: drop the "suppress_thinking=False to allow reasoning" note — `</think>` prefill is required for multi-image too. (See Critical methodology finding above.)
2. Mark V-M-TOOLS-DIAG `ui_diff`-specific scenarios as **gate-failed** with link to this file.
3. M-TOOLS-DIAG admits `diagnose_error` only.

---

## Reproduce

```bash
OLLAMA_URL=http://INTERNAL-HOST:11434 VLM_MODEL=qwen3-vl:8b \
  SMOKE_MODE=with_prefill .venv/bin/python eval_scripts/run_multi_image_smoke.py
```

Inputs: `eval_images/kombo/{01,02,07,08,10}_*.png` (already in repo).
Outputs: `eval_results/smoke_multi_image/pair_*.json`, `summary_*.json`, this file.
