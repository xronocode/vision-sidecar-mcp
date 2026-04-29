# After-Tuning Evaluation Report: 05_tablet_portrait_hero.png

## 1. Screenshot metadata
- viewport: 768×1024; tablet portrait hero
- reused exactly: yes; v0.2.2 + ML-team config

## 2. Previous baseline summary
- baseline neutral: 4.4; baseline structured: 4.6
- v0.2.0: required 2 attempts each; structured had role mis-tagging

## 3. New tuned MCP outputs summary
- **neutral**: succeeded first attempt. All visible text captured.
- **structured**: succeeded first attempt. Schema clean. **`appears_clipped: false`** with evidence "No visible content below the 'Join the parent waitlist →' link" — **wrong**: FOR TEACHERS section is below fold here (mild false negative).

## 4. Direct before/after comparison

| Dimension | Baseline N | New N | Baseline S | New S | Change |
|---|---|---|---|---|---|
| OCR/text extraction | 5 | 5 | 5 | 5 | unchanged |
| UI element detection | 5 | 5 | 5 | 5 | unchanged |
| layout understanding | 4 | 4 | 4 | 4 | unchanged |
| CTA/button detection | 5 | 5 | 5 | 5 | unchanged |
| semantic understanding | 5 | 5 | 4 | 5 | improved |
| hallucination control | 4 | 4 | 4 | 4 | unchanged |
| uncertainty handling | 4 | 4 | 4 | 3 (false negative on clipping) | regressed |
| usefulness for downstream | 4 | 4 | 5 | 4 | regressed |

## 5. Specific failure-mode check
- ✦ vs +: n/a
- clipping detection: FALSE NEGATIVE — model says no clipping despite FOR TEACHERS being below fold
- new errors: structured run is overconfident on "no clipping"

## 6. New scores

| Dimension | New N | New S |
|---|---:|---:|
| OCR/text extraction | 5 | 5 |
| UI element detection | 5 | 5 |
| layout understanding | 4 | 4 |
| CTA/button detection | 5 | 5 |
| semantic understanding | 5 | 5 |
| table extraction | n/a | n/a |
| hallucination control | 4 | 4 |
| uncertainty handling | 4 | 3 |
| usefulness for downstream | 4 | 4 |

## 7. Verdict
**Mixed**. Reliability fixed (no retries needed) but structured produces a confident false-negative on clipping.
