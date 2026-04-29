# After-Tuning Evaluation Report: 06_tablet_landscape_sections.png

## 1. Screenshot metadata
- viewport: 1024×768; 3 audience cards
- reused exactly: yes; v0.2.2 + ML-team config

## 2. Previous baseline summary
- baseline neutral: 4.4; baseline structured: 4.4
- key error: FOR TEACHERS asserted purple

## 3. New tuned MCP outputs summary
- **neutral**: succeeded first attempt (smaller output ~770B but content correct).
- **structured**: succeeded first attempt. Schema clean. → glyph captured for both waitlist links. FOR TEACHERS still color-tagged purple. `appears_clipped: false` correct.

## 4. Direct before/after comparison

| Dimension | Baseline N | New N | Baseline S | New S | Change |
|---|---|---|---|---|---|
| OCR/text extraction | 5 | 5 | 5 | 5 | unchanged |
| UI element detection | 5 | 5 | 5 | 5 | unchanged |
| layout understanding | 5 | 5 | 5 | 5 | unchanged |
| CTA/button detection | 5 | 5 | 5 | 5 | unchanged |
| semantic understanding | 4 | 4 | 4 | 5 | improved |
| hallucination control | 3 | 3 (FOR TEACHERS purple) | 3 | 3 | unchanged |
| uncertainty handling | 2 | 4 | 2 | 5 | improved |
| usefulness for downstream | 4 | 4 | 5 | 5 | unchanged |

## 5. Specific failure-mode check
- FOR TEACHERS color: NOT fixed
- clipping detection: improved (always reports)
- new errors: none

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
| uncertainty handling | 4 | 5 |
| usefulness for downstream | 4 | 5 |

## 7. Verdict
**Slightly improved**. Reliability up; FOR TEACHERS color still hallucinated.
