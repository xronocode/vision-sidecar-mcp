# Evaluation Report: 09_mobile_comparison_table.png

## 1. Screenshot metadata
- filename: `09_mobile_comparison_table.png`
- viewport: 390x844
- intended section: comparison table, mobile
- actual captured section: top half = 4 HOW IT WORKS step cards stacked vertically; bottom half = WHY KOMBO eyebrow + full comparison table (all 4 rows, both columns visible, with cell text wrapped over multiple lines)
- purpose: Mobile table behavior, possible overflow, OCR stress

## 2. Independent baseline analysis

**Visible text:**

Top: 4 HOW IT WORKS step cards stacked vertically (instead of horizontally as on desktop):
1. `Practice math` / `Solve problems at your level` (light purple)
2. `Earn ✦ Sparks` / `Every correct answer counts` (light yellow). Glyph is a 4-pointed spark, not "+"
3. `Build kingdom` / `Grow your world with sparks` (light teal)
4. `Want more` / `Unlock regions and earn rewards` (light pink)

`WHY KOMBO` (purple, letter-spaced eyebrow)

**Comparison table (mobile, narrow columns force cell text to wrap multiple lines):**

| (row label) | kombo | Prodigy |
|---|---|---|
| Scope | Focused on / math facts | Full curriculum / K-8 |
| Core skill | Speed and / retention | Conceptual / understanding |
| Complexity | Start in 5 / seconds | Setup and / onboarding |
| Philosophy | Free, no / ads, no / paywalls | Freemium with / membership |

The header `kombo` is bolder than `Prodigy` (subtle weight emphasis on the brand's own column).

**UI elements:** 4 step cards (vertical stack), 1 comparison table

**Layout structure:** Single mobile column. Step cards stack vertically (vs. desktop horizontal). Table is 3 columns: row label + kombo + Prodigy.

**Buttons/links:** none visible

**Table content:** as transcribed above

**Numbers visible:** `5` (in "5 seconds"), `K-8`

**Semantic meaning:** Mobile rendering of the desktop comparison

**Uncertainty notes:** None significant. Cell text wrapping is heavy due to narrow viewport — important stress test.

## 3. MCP neutral output summary

Excellent. Captured all 4 step cards (`Earn + Sparks` is still the recurrent OCR error). Reproduced the full table with all 4×2 cells correctly transcribed. Identified the `5` in "Start in 5 seconds". Said "background: white with black text" for the table — accurate. No truncation. Clean output.

## 4. MCP structured output summary

Schema followed cleanly. **`visible_text_exactly_as_seen` listed every cell value individually as flat list items** — the structure of the table is lost in the flat list, recovered only via the `table_content_if_present` field below. Captured both numbers correctly: `5` listed under `numbers_dates_amounts`. Markdown table emitted with all 8 cells correct + row labels. **However, `possible_layout_issues` again leaks subjective opinion:** claims "Complexity is not a standard metric for app comparison" — same opinion as in 03 structured, an interpretation injected as observation.

## 5. Comparison table

| Dimension | Independent baseline | MCP neutral | MCP structured | Notes |
|---|---|---|---|---|
| visible text extraction | All cell content + step cards verbatim | Complete (with ✦ → "+") | Complete via table field; flat list partial | Match on accuracy; structured weaker on preserving table-vs-flat-text distinction |
| UI element detection | 4 step cards + table | All detected | All detected | Match |
| layout understanding | Mobile vertical stack of cards + 3-col table | "Vertically stacked" cards (correct, vs. desktop horizontal) + "two-column" table (omits row label column) | Same description; markdown table includes row label column | Structured wins on table layout |
| CTA/button detection | none | "No interactive elements" | "No buttons" | Match |
| semantic understanding | Mobile rendering of comparison | Correct | Correct | Match |
| table extraction | 4 rows × 3 cols, cells with wrap | 4×2 markdown table (cells correct, row labels in body) | 4×3 markdown table (cells correct, row labels first col) | Both correct cells; structured cleaner |
| uncertainty handling | None significant | "All visible text explicitly transcribed" | "None visible" | Match |
| hallucinations | None | None | Subjective layout critique re-introduced | Structured leaks opinion |
| omissions | None | None | None | Match |

## 6. Error taxonomy

- **OCR/text errors:** ✦ → `+` (stable across the dataset)
- **numeric/date/amount errors:** Both runs caught `5`. Neutral did not have a numbers field but mentioned `5` in body. Structured caught `5` but missed `K-8` again
- **omissions:** Structured missed `K-8`
- **hallucinations:** Structured `possible_layout_issues` includes opinion-as-observation
- **wrong interpretation:** Structured's flat `visible_text_exactly_as_seen` strips the table structure
- **layout/positioning errors:** Neutral describes the table as 2-column (omitting row label column); structured uses markdown table that includes row labels — better
- **table extraction errors:** none on cell content; both perfect
- **uncertainty handling problems:** none significant
- **formatting/schema problems:** Structured's `possible_layout_issues` field acts as both observation and critique container — needs decoupling

## 7. Scores

| Dimension | MCP neutral | MCP structured |
|---|---|---|
| OCR/text extraction | 4 (✦ → "+") | 4 (✦ → "+") |
| UI element detection | 5 | 5 |
| layout understanding | 4 | 5 (markdown table is 3-col) |
| CTA/button detection | 5 | 5 |
| semantic understanding | 5 | 4 (subjective leak) |
| table extraction | 5 | 5 |
| hallucination control | 5 | 3 (subjective critique re-injected) |
| uncertainty handling | 4 | 4 |
| usefulness for downstream task | 4 | 5 (markdown table) |

## 8. Local recommendations for this screenshot

**What it did well:** Both runs **perfectly transcribed every cell of the comparison table** including narrow-column wrapped text. This is the strongest feature of the model.

**What it missed:** `K-8` in structured numbers field; ✦ vs "+"; structured re-introduced subjective critique.

**Did structured prompting help?** Yes for the table (markdown format with row labels). Mixed for everything else.

**What would help:** (1) prompt-level constraint to **list table cells inside a `table` field only**, not duplicated in the flat text field; (2) split `possible_layout_issues` into `observed_layout_anomalies` and `subjective_critique` (and instruct model to leave the latter empty); (3) again — close `image_type` to a small enum; (4) for narrow-cell tables, ask the model to transcribe each cell as **a single string with wraps removed**, not multi-line.
