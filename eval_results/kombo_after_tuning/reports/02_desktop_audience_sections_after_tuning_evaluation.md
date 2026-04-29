# After-Tuning Evaluation Report: 02_desktop_audience_sections.png

## 1. Screenshot metadata
- viewport: 1440×900; audience cards section
- reused exactly: yes; v0.2.2 + ML-team config

## 2. Previous baseline summary
- previous neutral: 3.7 avg; previous structured: 3.7 avg
- key errors: ✦ → +; FOR TEACHERS asserted as purple

## 3. New tuned MCP outputs summary
- **neutral** (succeeded first attempt): captured all 3 audience cards + 4 step cards. **`Earn + Sparks` still misread** in neutral. FOR TEACHERS still asserted "purple". States "no clipping" — correct.
- **structured** (succeeded first attempt): clean schema. **✦ correctly preserved** in `Earn ✦ Sparks` block_id and `glyphs_and_icons` entry. FOR TEACHERS still purple. `appears_clipped: false` correct. → glyph also captured.

## 4. Direct before/after comparison

| Dimension | Baseline N | New N | Baseline S | New S | Change |
|---|---|---|---|---|---|
| OCR/text extraction | 4 | 4 (✦→+ in neutral) | 4 | 5 (✦ correct) | structured improved |
| UI element detection | 5 | 5 | 5 | 5 | unchanged |
| layout understanding | 4 | 4 | 4 | 4 | unchanged |
| CTA/button detection | 5 | 5 | 5 | 5 | unchanged |
| semantic understanding | 4 | 4 | 4 | 5 (no opinion leak) | improved |
| hallucination control | 3 | 3 (FOR TEACHERS purple) | 3 | 3 (FOR TEACHERS purple) | unchanged |
| uncertainty handling | 2 | 4 (states clipping correctly) | 2 | 4 (`appears_clipped` populated) | improved |
| usefulness for downstream | 4 | 4 | 4 | 5 | improved |

## 5. Specific failure-mode check
- ✦ vs +: **fixed in structured**, still wrong in neutral
- FOR TEACHERS color: NOT fixed (still purple in both runs)
- clipping detection: improved
- subjective leak: fixed (`subjective_notes: null`)
- new errors: none

## 6. New scores

| Dimension | New N | New S |
|---|---:|---:|
| OCR/text extraction | 4 | 5 |
| UI element detection | 5 | 5 |
| layout understanding | 4 | 4 |
| CTA/button detection | 5 | 5 |
| semantic understanding | 4 | 5 |
| table extraction | n/a | n/a |
| hallucination control | 3 | 3 |
| uncertainty handling | 4 | 4 |
| usefulness for downstream | 4 | 5 |

## 7. Verdict
**Improved**. Structured run captures ✦ correctly. FOR TEACHERS color hallucination unchanged.
