# After-Tuning Evaluation Report: 08_mobile_audience_sections.png

## 1. Screenshot metadata
- viewport: 390×844; 3 audience cards stacked
- reused exactly: yes; v0.2.2 + ML-team config

## 2. Previous baseline summary
- baseline neutral: 4.4; baseline structured: 4.0 (sentence-split bug)
- v0.2.0: required retries

## 3. New tuned MCP outputs summary
- **neutral**: succeeded first attempt. Joins wrapped sentences correctly (no sentence-split bug). FOR TEACHERS still purple.
- **structured**: succeeded first attempt. **`appears_clipped: true`** with evidence about content extending below — correct. → glyph captured. FOR TEACHERS still purple.

## 4. Direct before/after comparison

| Dimension | Baseline N | New N | Baseline S | New S | Change |
|---|---|---|---|---|---|
| OCR/text extraction | 5 | 5 | 4 (sentence split) | 5 (joined) | improved |
| UI element detection | 5 | 5 | 5 | 5 | unchanged |
| layout understanding | 5 | 5 | 5 | 5 | unchanged |
| CTA/button detection | 5 | 5 | 5 | 5 | unchanged |
| semantic understanding | 4 | 4 | 4 | 5 | improved |
| hallucination control | 3 | 3 | 3 | 3 | unchanged |
| uncertainty handling | 3 | 5 | 3 | 5 | improved |
| usefulness for downstream | 4 | 5 | 4 | 5 | improved |

## 5. Specific failure-mode check
- sentence-split bug: **fixed**
- clipping detection: improved
- FOR TEACHERS color: NOT fixed

## 6. New scores

| Dimension | New N | New S |
|---|---:|---:|
| OCR/text extraction | 5 | 5 |
| UI element detection | 5 | 5 |
| layout understanding | 5 | 5 |
| CTA/button detection | 5 | 5 |
| semantic understanding | 4 | 5 |
| table extraction | n/a | n/a |
| hallucination control | 3 | 3 |
| uncertainty handling | 5 | 5 |
| usefulness for downstream | 5 | 5 |

## 7. Verdict
**Improved**. All deltas positive; FOR TEACHERS color still hallucinated.
