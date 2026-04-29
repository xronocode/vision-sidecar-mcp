# After-Tuning Evaluation Report: 09_mobile_comparison_table.png

## 1. Screenshot metadata
- viewport: 390×844; step cards + comparison table (mobile)
- reused exactly: yes; v0.2.2 + ML-team config

## 2. Previous baseline summary
- baseline neutral: 4.4; baseline structured: 4.4 (subjective leak)

## 3. New tuned MCP outputs summary
- **neutral**: succeeded first attempt. **✦ correctly preserved** in `Earn ✦ Sparks`. Full table cells correct. Notes "table 4×3" (with row labels) — correct.
- **structured**: succeeded first attempt. **✦ preserved** in block_id and `glyphs_and_icons`. Full `table_content` with row labels and all 8 cells correct. `numbers_dates_amounts` populated with `5`. **`appears_clipped: true`** with "Table content extends beyond visible area" — **wrong**, full table is visible (false positive).
- **extract_table**: succeeded (4 rows × 3 cols, all cells correct).

## 4. Direct before/after comparison

| Dimension | Baseline N | New N | Baseline S | New S | Change |
|---|---|---|---|---|---|
| OCR/text extraction | 4 (✦→+) | 5 (✦ correct) | 4 | 5 | **improved both** |
| UI element detection | 5 | 5 | 5 | 5 | unchanged |
| layout understanding | 4 | 5 (3-col table) | 5 | 5 | improved (neutral) |
| CTA/button detection | 5 | 5 | 5 | 5 | unchanged |
| semantic understanding | 5 | 5 | 4 (subjective leak) | 5 | improved |
| table extraction | 5 | 5 | 5 | 5 | unchanged |
| hallucination control | 5 | 5 | 3 | 4 (false-clipped) | mixed |
| uncertainty handling | 4 | 4 | 4 | 3 (false positive) | regressed |
| usefulness for downstream | 4 | 5 | 5 | 5 | improved |

## 5. Specific failure-mode check
- ✦ vs +: **FIXED in both runs** (first time in dataset for this image)
- subjective leak: **fixed**
- clipping detection: structured has false-positive (says clipped though table is visible)
- table extraction (extract_table): perfect

## 6. New scores

| Dimension | New N | New S | extract_table |
|---|---:|---:|---:|
| OCR/text extraction | 5 | 5 | 5 |
| UI element detection | 5 | 5 | n/a |
| layout understanding | 5 | 5 | 5 |
| CTA/button detection | 5 | 5 | n/a |
| semantic understanding | 5 | 5 | n/a |
| table extraction | 5 | 5 | 5 |
| hallucination control | 5 | 4 (false-clipped) | 5 |
| uncertainty handling | 4 | 3 | 5 |
| usefulness for downstream | 5 | 5 | 5 |

## 7. Verdict
**Improved**. ✦ glyph fixed in BOTH runs (best of dataset). Minor: structured run wrongly flags clipping.
