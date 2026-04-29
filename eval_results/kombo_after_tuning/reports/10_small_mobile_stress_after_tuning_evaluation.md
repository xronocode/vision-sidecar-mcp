# After-Tuning Evaluation Report: 10_small_mobile_stress.png

## 1. Screenshot metadata
- viewport: 320×568; small-mobile stress (CTAs below fold)
- reused exactly: yes; v0.2.2 + ML-team config + image upscaled 2× via Lanczos

## 2. Previous baseline summary
- baseline neutral: 3.4 (worst-performing); baseline structured: 3.1
- baseline 1/5 uncertainty (asserted "no issues"); v0.2.0 fixed to 5/5

## 3. New tuned MCP outputs summary
- **neutral**: succeeded first attempt (1.7 KB content). Notes clipping. Still says "centered" alignment in places (centered-vs-left issue persists).
- **structured**: succeeded first attempt. **`appears_clipped: true`** with evidence "Hero section has heading and subhead but no primary action button below subhead" — correct. `expected_missing_elements` lists "Start playing" + alternatives.

## 4. Direct before/after comparison

| Dimension | Baseline N | New N | Baseline S | New S | Change |
|---|---|---|---|---|---|
| OCR/text extraction | 5 | 5 | 5 | 5 | unchanged |
| UI element detection | 4 | 4 | 4 | 5 | improved |
| layout understanding | 2 | 5 | 2 | 5 | **strongly improved both** |
| CTA/button detection | 5 | 5 | 5 | 5 | unchanged |
| semantic understanding | 4 | 4 | 4 | 5 | improved |
| hallucination control | 3 | 3 (centered claim) | 3 | 3 | unchanged |
| uncertainty handling | 1 | 5 | 1 | 5 | **strongly improved** |
| usefulness for downstream | 2 | 5 | 2 | 5 | **strongly improved** |

## 5. Specific failure-mode check
- clipping detection: **strongly improved** (1/5 → 5/5 in both runs)
- centered-vs-left alignment: still claimed in places (model bias)

## 6. New scores

| Dimension | New N | New S |
|---|---:|---:|
| OCR/text extraction | 5 | 5 |
| UI element detection | 4 | 5 |
| layout understanding | 5 | 5 |
| CTA/button detection | 5 | 5 |
| semantic understanding | 4 | 5 |
| table extraction | n/a | n/a |
| hallucination control | 3 | 3 |
| uncertainty handling | 5 | 5 |
| usefulness for downstream | 5 | 5 |

## 7. Verdict
**Strongly improved**. The dataset's worst-served screenshot in cycle 1 is now a top performer.
