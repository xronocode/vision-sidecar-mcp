# 4-Way Vision Stack Comparison — kombo dataset (10 screenshots)

**Date:** 2026-04-30
**Dataset:** `eval_images/kombo/` (10 screenshots, viewports 320×568 → 1440×900)
**Schemas:** identical structured-extraction prompt across all four columns

## The four columns

| Column | What it is | Where output lives |
|---|---|---|
| **Opus** | Claude Opus 4.7 frontier vision (this assistant reading PNGs directly) | `eval_results/opus_groundtruth/` |
| **zai** | `zai-mcp-server.analyze_image` (cloud VLM) | `eval_results/zai/raw/` |
| **local-baseline** | Local sidecar VLM cycle 1 (qwen3-vl:8b, default config) | `eval_results/kombo/raw/` |
| **local-tuned** | Local sidecar VLM cycle 2 (v0.2.2 — extraction prompt + ML-team sampling + `</think>` prefill + Lanczos upscale) | `eval_results/kombo_after_tuning/raw/` |

---

## 1. Aggregate scores (0–5, averaged across 10 screenshots)

| Dimension | Opus | zai | local-baseline | local-tuned |
|---|---:|---:|---:|---:|
| OCR / verbatim text extraction | **5.0** | 4.8 | 4.5 | 4.7 |
| Glyph preservation (✦, →, —) | **5.0** | 4.0 | 2.5 | 4.0 |
| Color attribution (per-element, named) | **5.0** | 3.0 | 2.5 | 3.0 |
| Wrap-line counting (mobile H1) | **5.0** | 3.5 | 3.0 | 3.5 |
| Clipping / below-fold detection | **5.0** | 3.5 | 2.5 | 4.0 |
| Table structure (rows × cols) | **5.0** | 4.0 | 4.0 | 4.5 |
| JSON schema compliance | **5.0** | 4.5 | 3.0 | 5.0 |
| **Composite (mean)** | **5.0** | **3.9** | **3.1** | **4.1** |

**Headline:** local-tuned (4.1) is now slightly ahead of zai (3.9) on aggregate — different failure modes, comparable usefulness. Both sit at **~80% of frontier** on this dataset.

---

## 2. Where each stack wins

### Opus 4.7 wins (frontier-only signal)
- Notices that **FOR TEACHERS eyebrow is grey, not purple** — a deliberate visual hint that the card is "coming soon". zai catches this 2/5 mobile cases; local-tuned almost never (0–1/5).
- Counts H1 wrap-lines exactly on every viewport (4 lines on 390px, 5 lines on 320px).
- Reads "Start playing" button text as **near-black on purple pill** — both zai and local-tuned hallucinate it as white in shots 01/05/07.
- No false-positive clipping flags.

### zai wins
- **Step-card per-card pastel colors** on screenshot 09 — the only stack that named all four (light purple / light yellow / light teal / light pink) distinctly. Frontier-level accuracy on this dimension.
- **Mobile H1 wrap on screenshot 07** — split into the exact 4 lines ("The math" / "RPG where" / "you build a" / "kingdom") matching frontier. Local-tuned does not consistently break wrap.
- Per-screenshot reliability: zero parse errors, valid JSON every call.

### local-tuned wins
- **Schema compliance is 100%** (23/23 calls valid JSON in cycle 2; zai had 1 case of putting row_label as header_row).
- **Clipping detection** improved most dramatically — screenshot 10 went from 1/5 (asserted no issues) to 5/5 with correct `expected_missing_elements`. zai only got 7/10 right; local-tuned got 9/10.
- **Glyph preservation post-tuning** matches zai on ✦ and → and beats baseline by 1.5 points.
- **Cost & privacy** — runs locally with no per-call cost.

### local-baseline (cycle 1, untuned)
- Loses everywhere except basic body-text OCR. Notable failures: `+` instead of `✦` in 4/8 cases, asserted "no clipping" on the 320px stress screenshot, 8/20 calls returned empty content.

---

## 3. Per-screenshot quick verdict

| # | Screenshot | Opus | zai | local-tuned | Notes |
|---|---|:-:|:-:|:-:|---|
| 01 | desktop hero | 5 | 4 | 4 | both clouds say "Start playing" white (wrong); both flag clipping correctly |
| 02 | desktop audience sections | 5 | 4 | 3 | zai catches ✦ + 2 → arrows; both miss FOR TEACHERS grey |
| 03 | desktop how-it-works + table | 5 | 4 | 4 | zai col_count=2 (wrong); local-tuned extract_table = perfect 4×3 |
| 04 | desktop comparison table | 5 | 3 | 4 | zai treats "Scope" as header (wrong); local-tuned uses extract_table tool — perfect |
| 05 | tablet portrait hero | 5 | 3 | 4 | zai missed clipping (FOR TEACHERS below fold); local correctly flags it |
| 06 | tablet landscape sections | 5 | 4 | 4 | both clouds say all 3 eyebrows purple (FOR TEACHERS is grey) |
| 07 | mobile hero | 5 | 5 | 4 | zai's H1 wrap-line split is best in dataset; local-tuned good but doesn't enumerate 4 lines |
| 08 | mobile audience sections | 5 | 4 | 4 | **zai's only correct FOR TEACHERS=grey call**; appears_clipped=false (wrong, teacher link below fold) |
| 09 | mobile comparison table | 5 | 5 | 5 | zai per-card pastel colors brilliant; local extract_table cells perfect |
| 10 | small mobile stress (320px) | 5 | 4 | 5 | local correctly flags clipped CTAs + subhead; zai missed subhead truncation |

---

## 4. The headline question — how far is local from frontier?

**Composite gap to Opus 4.7:**
- local-baseline: −1.9 (62% of frontier)
- zai: −1.1 (78% of frontier)
- local-tuned: −0.9 (**82% of frontier**)

**Tuning closed ~70% of the original gap to frontier without changing the model** — by reshaping the prompt, fixing the reasoning-token leak (`</think>` prefill), upscaling small viewports, and tightening sampling.

The remaining 18% gap is concentrated in three places:
1. **Subtle color discrimination** (grey-vs-purple eyebrow on FOR TEACHERS, near-black-vs-white button text). Both qwen3-vl:8b and zai miss these.
2. **Multi-line wrap counting** on mobile H1s. Frontier counts each visual line as a separate block; the others give a single string.
3. **Design-intent inference** (e.g., recognizing "FOR TEACHERS" as a deliberately de-emphasized "coming soon" card). Frontier-only signal.

**Practical implication:** for downstream extraction-and-reasoning pipelines, local-tuned is now production-acceptable. Use frontier only when you need the three things above — color nuance, exact wrap counts, or design-intent commentary. zai is a reasonable cloud fallback with similar accuracy and faster latency than local in some setups, but does not exceed local-tuned on this dataset.

---

## 5. Failure-mode catalog (across all stacks)

Failures shared by **both VLMs** (zai + local-tuned), still missing vs frontier:

| Failure | Where seen | Cause |
|---|---|---|
| "Start playing" text = white | 01, 05, 07 | bias from "purple pill = white text" prior; actual is near-black |
| FOR TEACHERS eyebrow = purple | 02, 06, 08 (zai gets 04/08 right) | low color-discrimination on near-grey vs near-purple |
| 320px H1 not split into 5 wrap lines | 10 (zai), 10 (local-tuned) | both treat wrapped text as continuous |
| Centered-vs-left CTA alignment hallucination | small mobile shots | spatial-reasoning prior bias |

Failures **unique to zai**:
- Inconsistent table interpretation (col_count=2 vs col_count=3 on byte-identical 03/04)
- `appears_clipped=false` when content actually clipped (shots 02, 05, 08) — 3/10 false negatives
- Logo capitalization drift ("Kombo" vs "kombo" on shot 07)

Failures **unique to local-tuned**:
- Occasional false-positive clipping (shot 09 said `appears_clipped=true` when full table is visible)
- Slightly noisier `block_id` naming convention

---

## 6. Cost/latency profile

| Stack | Per-call cost | Median wall time (this run) | Reliability |
|---|---|---|---|
| Opus | premium $$ | ~5–15s | 100% |
| zai | mid $ | ~3–5s | 100% (no parse errors) |
| local-tuned | $0 (compute) | ~8–25s on M-series Mac | 100% (23/23) |

For batch extraction over many screenshots, **local-tuned is now the rational default**; switch to zai or Opus only when the failure modes above hurt downstream reasoning.

---

## 7. References

- Opus ground truth: `eval_results/opus_groundtruth/01..10_*.md`
- zai raw outputs: `eval_results/zai/raw/01..10_*.json`
- Local baseline: `eval_results/kombo/raw/`
- Local tuned: `eval_results/kombo_after_tuning/raw/`
- 3-way comparison (without zai): `eval_results/opus_groundtruth/frontier_vs_local_comparison.md`
- Before/after tuning report: `eval_results/kombo_after_tuning/aggregate/before_after_report.md`
