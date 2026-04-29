# After-Tuning Evaluation Report: 01_desktop_hero.png

## 1. Screenshot metadata
- filename: `01_desktop_hero.png`
- viewport: 1440×900
- previous intended section: top of page (hero)
- previous actual captured section: hero card + start of FOR KIDS / FOR PARENTS below the fold
- reused exactly from original dataset: yes
- server config: v0.2.2 with ML-team sampling (seed=42, top_p=0.9, top_k=20, repeat_penalty=1.05, num_predict=8192, num_ctx=32768) + `</think>` prefill

## 2. Previous baseline summary
- previous neutral score (avg): 3.7 (truncated)
- previous structured score (avg): 4.2

## 3. New tuned MCP outputs summary
- **new neutral**: succeeded first attempt (13.67s — 3× faster than v0.2.0 retry's 50s). Captures all visible text. Text alignment correctly stated as **left-aligned** throughout. Identifies the purple oval shape next to the paragraph. **However asserts "no clipping at the bottom"** — wrong, FOR PARENTS body is clipped. Mild regression vs v0.2.0 neutral on this dimension.
- **new structured**: succeeded first attempt. Schema followed cleanly. **`appears_clipped: true`** with evidence "The 'FOR PARENTS' section is partially visible with text cut off at the bottom" — correct. Em-dash glyph captured. Purple egg shape listed. `numbers_dates_amounts: []` (correct).

## 4. Direct before/after comparison

| Dimension | Baseline neutral | New neutral (v0.2.2) | Baseline structured | New structured (v0.2.2) | Change |
|---|---|---|---|---|---|
| OCR/text extraction | 3 (truncated) | 5 | 5 | 5 | improved |
| UI element detection | 4 | 5 (egg shape listed) | 4 | 5 | improved |
| layout understanding | 3 (no 2-col hero) | 4 (notes egg right of paragraph) | 3 | 4 | improved |
| CTA/button detection | 5 | 5 | 5 | 5 | unchanged |
| semantic understanding | 5 | 5 | 5 | 5 | unchanged |
| hallucination control | 3 | 4 (no hex, alignment correct) | 4 | 4 | improved |
| uncertainty handling | 3 | 3 (false "not clipped") | 4 | 5 (correct clipping flag) | mixed |
| usefulness for downstream | 3 | 4 | 4 | 5 | improved |

## 5. Specific failure-mode check
- ✦ vs +: n/a (no ✦ on this image)
- color hallucination: improved (no hex, alignment correctly left)
- clipping detection: **structured = correct**; neutral now wrongly says "not clipped" (regression on neutral). Mixed.
- table extraction: n/a
- structured more useful: yes
- new errors: neutral run mis-flags clipping. Likely seed-driven sampling change.

## 6. New scores

| Dimension | New MCP neutral | New MCP structured |
|---|---:|---:|
| OCR/text extraction | 5 | 5 |
| UI element detection | 5 | 5 |
| layout understanding | 4 | 4 |
| CTA/button detection | 5 | 5 |
| semantic understanding | 5 | 5 |
| table extraction | n/a | n/a |
| hallucination control | 4 | 4 |
| uncertainty handling | 3 | 5 |
| usefulness for downstream | 4 | 5 |

## 7. Verdict for this screenshot
**Improved**. Both runs faster, neutral fully complete (no truncation). Structured perfectly handles clipping. Slight regression on neutral clipping detection.
