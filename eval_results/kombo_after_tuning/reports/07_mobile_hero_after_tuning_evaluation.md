# After-Tuning Evaluation Report: 07_mobile_hero.png

## 1. Screenshot metadata
- viewport: 390×844; mobile hero
- reused exactly: yes; v0.2.2 + ML-team config + auto-prefill `</think>`

## 2. Previous baseline summary
- baseline neutral: 3.8 (truncated); baseline structured: 4.3
- v0.2.0: structured succeeded with CTA wrap correctly identified; **neutral with viewport_hint=mobile EMPTY 8/8 attempts** (deterministic regression)

## 3. New tuned MCP outputs summary
- **neutral with `viewport_hint=mobile`**: **succeeded first attempt (31.64s)** — the deterministic empty-response failure is FIXED. Captures top bar + hero card + "FOR KIDS" partial section. **Notes "Content extends below the visible fold"** correctly. Correctly identifies that `Start playing/I'm a parent/I'm a teacher` are stacked vertically. Top nav buttons described as "light purple background, white text" — wrong (they're white background, dark text).
- **structured**: succeeded first attempt. Schema clean. CTA layout captured. **`appears_clipped: true`** with evidence about FOR KIDS body cut off.

## 4. Direct before/after comparison

| Dimension | Baseline N | New N | Baseline S | New S | Change |
|---|---|---|---|---|---|
| OCR/text extraction | 4 (truncated) | 5 | 5 | 5 | improved |
| UI element detection | 4 | 5 | 4 | 5 | improved |
| layout understanding | 3 (no CTA wrap) | 5 (CTA stacking captured) | 3 | 5 | improved |
| CTA/button detection | 5 | 5 | 5 | 5 | unchanged |
| semantic understanding | 5 | 5 | 5 | 5 | unchanged |
| hallucination control | 3 | 3 (top nav bg color wrong) | 4 | 4 | unchanged |
| uncertainty handling | 2 | 5 (clipping flagged) | 5 | 5 | improved |
| usefulness for downstream | 3 | 5 | 4 | 5 | improved |

## 5. Specific failure-mode check
- ✦ vs +: n/a
- empty-response on mobile hint: **FIXED** (was 8/8 empty)
- CTA wrap detection: **fixed**
- clipping detection: improved
- new errors: top nav button background color claim slightly off

## 6. New scores

| Dimension | New N | New S |
|---|---:|---:|
| OCR/text extraction | 5 | 5 |
| UI element detection | 5 | 5 |
| layout understanding | 5 | 5 |
| CTA/button detection | 5 | 5 |
| semantic understanding | 5 | 5 |
| table extraction | n/a | n/a |
| hallucination control | 3 | 4 |
| uncertainty handling | 5 | 5 |
| usefulness for downstream | 5 | 5 |

## 7. Verdict
**Strongly improved**. The 8/8 empty deterministic failure is gone.
