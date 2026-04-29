# After-Tuning Evaluation Report: 03_desktop_how_it_works.png

## 1. Screenshot metadata
- viewport: 1440×900; HOW IT WORKS + WHY KOMBO (page bottoms out, byte-identical to 04)
- reused exactly: yes; v0.2.2 + ML-team config

## 2. Previous baseline summary
- baseline neutral: 4.3; baseline structured: 4.2 (subjective leak)
- v0.2.0 retry pass: structured EMPTY 8/8 attempts (deterministic failure)

## 3. New tuned MCP outputs summary
- **neutral**: succeeded first attempt. All visible text including the WHY KOMBO comparison table captured. Notes table as "4 rows × 3 columns (row-label column present)". **`Earn + Sparks`** misread in neutral. FOR TEACHERS still called purple in this run.
- **structured**: **succeeded first attempt** (was 8/8 empty in v0.2.0). 10 KB of valid JSON. **✦ preserved correctly** in `Earn ✦ Sparks` + `glyphs_and_icons`. **FOR TEACHERS correctly classified as `dark grey`** — color hallucination FIXED here. All 8 table cells correct in `table_content`. `subjective_notes: null` — no leak. `appears_clipped: false` — correct (page bottoms out, no real clipping).
- **extract_table**: succeeded (5 rows × 3 cols — model includes header_row in row_count, off-by-one but cell content correct).

## 4. Direct before/after comparison

| Dimension | Baseline N | New N | Baseline S | New S | Change |
|---|---|---|---|---|---|
| OCR/text extraction | 4 | 4 (✦→+) | 4 | 5 (✦ correct) | structured improved |
| UI element detection | 5 | 5 | 5 | 5 | unchanged |
| layout understanding | 4 | 5 (3-col table) | 4 | 5 (table_content populated) | improved |
| CTA/button detection | 5 | 5 | 5 | 5 | unchanged |
| semantic understanding | 5 | 5 | 4 (subjective leak) | 5 (clean) | improved |
| table extraction | 5 | 5 | 5 | 5 | unchanged |
| hallucination control | 4 | 4 (FOR TEACHERS purple in N) | 3 | 5 (FOR TEACHERS dark grey in S) | improved |
| uncertainty handling | 3 | 4 | 3 | 5 | improved |
| usefulness for downstream | 4 | 4 | 5 | 5 | unchanged |

## 5. Specific failure-mode check
- ✦ vs +: **fixed in structured**, neutral still misreads
- FOR TEACHERS color: **FIXED in structured run** (`dark grey`); still purple in neutral
- clipping detection: correct in both
- empty response: **FIXED** (was 8/8 empty, now 0/2)
- subjective leak: **fixed**

## 6. New scores

| Dimension | New N | New S | extract_table |
|---|---:|---:|---:|
| OCR/text extraction | 4 | 5 | 5 |
| UI element detection | 5 | 5 | n/a |
| layout understanding | 5 | 5 | 4 (row_count off-by-one) |
| CTA/button detection | 5 | 5 | n/a |
| semantic understanding | 5 | 5 | n/a |
| table extraction | 5 | 5 | 4 |
| hallucination control | 4 | 5 | 5 |
| uncertainty handling | 4 | 5 | 5 |
| usefulness for downstream | 4 | 5 | 5 |

## 7. Verdict
**Strongly improved**. Empty-response failure fully fixed. Structured run is the strongest of the dataset on this image — ✦ + FOR TEACHERS color + table content all correct.
