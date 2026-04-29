# After-Tuning Evaluation Report: 04_desktop_comparison_table.png

## 1. Screenshot metadata
- viewport: 1440×900; byte-identical to 03 (page bottoms out)
- reused exactly: yes; v0.2.2 + ML-team config

## 2. Previous baseline summary
- baseline 04 was the **best run of cycle 1** (structured avg 4.7) — both numbers + clean markdown table
- v0.2.0: structured EMPTY 8/8; neutral truncated mid-output

## 3. New tuned MCP outputs summary
- **neutral**: succeeded (was truncating in v0.2.0). Captures full WHY KOMBO table. **`Earn + Sparks`** misread.
- **structured**: succeeded (was 8/8 empty). 10 KB of valid JSON. **✦ correctly preserved**. `numbers_dates_amounts` populated with `5 seconds` and `K-8`. Full `table_content` with row labels.
- **extract_table**: succeeded (4 rows × 3 cols, all cells correct).

## 4. Direct before/after comparison

| Dimension | Baseline N | New N | Baseline S | New S | Change |
|---|---|---|---|---|---|
| OCR/text extraction | 4 | 4 (✦→+) | 4 | 5 (✦ correct) | improved |
| UI element detection | 5 | 5 | 5 | 5 | unchanged |
| layout understanding | 4 | 5 | 5 | 5 | unchanged |
| CTA/button detection | 5 | 5 | 5 | 5 | unchanged |
| semantic understanding | 5 | 5 | 5 | 5 | unchanged |
| table extraction | 4 | 5 | 5 | 5 | improved |
| hallucination control | 5 | 5 | 5 | 5 | unchanged |
| uncertainty handling | 3 | 4 | 3 | 5 | improved |
| usefulness for downstream | 4 | 5 | 5 | 5 | improved |

## 5. Specific failure-mode check
- ✦ vs +: **fixed in structured**
- empty response: **FIXED**
- table extraction: extract_table dominates (5/5)
- determinism on 03/04 byte-identical pair: outputs are very similar (sampled with seed=42), structured cell content identical between 03 and 04

## 6. New scores

| Dimension | New N | New S | extract_table |
|---|---:|---:|---:|
| OCR/text extraction | 4 | 5 | 5 |
| UI element detection | 5 | 5 | n/a |
| layout understanding | 5 | 5 | 5 |
| CTA/button detection | 5 | 5 | n/a |
| semantic understanding | 5 | 5 | n/a |
| table extraction | 5 | 5 | 5 |
| hallucination control | 5 | 5 | 5 |
| uncertainty handling | 4 | 5 | 5 |
| usefulness for downstream | 5 | 5 | 5 |

## 7. Verdict
**Improved**. Empty-response failure fully resolved. Best structured run in dataset on this image.
