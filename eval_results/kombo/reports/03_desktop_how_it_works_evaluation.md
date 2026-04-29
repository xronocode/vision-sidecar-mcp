# Evaluation Report: 03_desktop_how_it_works.png

## 1. Screenshot metadata
- filename: `03_desktop_how_it_works.png`
- viewport: 1440x900
- intended section: HOW IT WORKS
- actual captured section: tail of FOR PARENTS waitlist link + full FOR TEACHERS card + HOW IT WORKS strip with 4 step cards + WHY KOMBO comparison table
- purpose: Step sequence, icons, process interpretation
- **note:** identical pixels to 04 (page bottoms out at maxScroll=973, so HOW IT WORKS and WHY KOMBO appear together in viewport)

## 2. Independent baseline analysis

**Visible text (top to bottom):**
- Top: `Join the parent waitlist →` (purple link, tail of previous section)
- Card: `FOR TEACHERS` (grey/muted eyebrow, **not purple**) / `Zero prep, full visibility` / paragraph / `Join the teacher waitlist →` (purple)
- `HOW IT WORKS` (purple eyebrow)
- 4 step cards in a single row:
  1. `Practice math` / `Solve problems at your level` (light purple)
  2. `Earn ✦ Sparks` / `Every correct answer counts` (light yellow). The glyph between "Earn" and "Sparks" is a 4-pointed spark (✦), not a "+"
  3. `Build kingdom` / `Grow your world with sparks` (light teal)
  4. `Want more` / `Unlock regions and earn rewards` (light pink)
- `WHY KOMBO` (purple eyebrow)
- Comparison table (header row + 4 data rows × 2 brand columns + row label column):
  - Header: blank cell | `kombo` | `Prodigy`
  - `Scope` | `Focused on math facts` | `Full curriculum K-8`
  - `Core skill` | `Speed and retention` | `Conceptual understanding`
  - `Complexity` | `Start in 5 seconds` | `Setup and onboarding`
  - `Philosophy` | `Free, no ads, no paywalls` | `Freemium with membership`

**UI elements:** 1 audience card (teachers), 4 step cards, 1 comparison table

**Layout structure:** Vertical stack of full-width sections; the 4 step cards are arranged in a 4-col grid; the table is a 3-column grid (row label + 2 brand columns)

**Buttons/links:** 2 inline waitlist links (`Join the parent waitlist →`, `Join the teacher waitlist →`)

**Table content:** as transcribed above. 4 rows × 2 brand columns; row labels `Scope`, `Core skill`, `Complexity`, `Philosophy`

**Numbers:** `5` (in "Start in 5 seconds"); `K-8` (in "Full curriculum K-8")

**Semantic meaning:** Marketing comparison — kombo as fast/free/focused vs. Prodigy as broad/freemium

**Uncertainty notes:** FOR TEACHERS eyebrow is intentionally muted, distinct from the purple HOW IT WORKS / WHY KOMBO eyebrows.

## 3. MCP neutral output summary

Faithful, complete description. Captured all 4 step cards with their colors. Read `Earn + Sparks` instead of `Earn ✦ Sparks` (OCR error on glyph). Reproduced full comparison table with all 8 cells correct. Output was truncated at the very end ("explicitly") but only after delivering all substantive content. Described the FOR TEACHERS eyebrow as "uppercase, smaller font, gray text" — **correctly noted as gray** here (more accurate than report 02). The HOW IT WORKS eyebrow color it correctly identified as purple.

## 4. MCP structured output summary

Excellent table extraction — perfect markdown table with all 4 rows × 2 cols. Identified `5 seconds` as a number under `numbers_dates_amounts`, but **missed `K-8`** that 04 structured caught. Also misread `Earn ✦ Sparks` → `Earn + Sparks`. Schema followed cleanly. `image_type` field overshares ("UI screenshot of a webpage for an educational platform (Kombo), featuring promotional content for teachers and a comparison with Prodigy.") — that's interpretation slipping into the type field, not a strict classification.

## 5. Comparison table

| Dimension | Independent baseline | MCP neutral | MCP structured | Notes |
|---|---|---|---|---|
| visible text extraction | All visible verbatim | Complete (with ✦ → "+" error) | Complete (with ✦ → "+" error) | Tie |
| UI element detection | 1 card + 4 step cards + table + 2 links | All detected | All detected | Match |
| layout understanding | Stacked sections; 4-col card grid; 3-col table | Sections stacked; cards horizontal; table 2-col | Sections stacked; cards horizontal; table 2-col | Both treat table as 2-col, ignoring row-label column as a third column |
| CTA/button detection | 2 inline links | 2 links identified | 2 links identified | Match |
| semantic understanding | Comparison framing kombo vs Prodigy | Correct | Correct, but pads the image_type field | Structured contaminates `image_type` with semantic interpretation |
| table extraction | 4 rows × 3 cols (with row labels) | Captured all data correctly | Captured all data correctly via markdown table | Match. Both got cell content right |
| uncertainty handling | Note FOR TEACHERS color | "All text legible" / no uncertainty flagged | "None visible" | Both miss the muted teacher eyebrow color (less wrong here — neutral did say "gray text") |
| hallucinations | None | None substantive | Added subjective layout critique under `possible_layout_issues` ("Complexity is not a standard metric") — opinion, not observation | Structured leaks opinion into the schema |
| omissions | None | Loss of "explicitly" final word | Missed `K-8` as a number | Both have minor omissions |

## 6. Error taxonomy

- **OCR/text errors:** ✦ → `+` in both runs
- **numeric/date/amount errors:** Structured missed `K-8`; neutral did not have a numbers field but mentioned "5 seconds" only
- **omissions:** Trivial truncation in neutral; missed `K-8` in structured numbers field
- **hallucinations:** Structured `possible_layout_issues` invents a critique ("Complexity is not a standard metric for app comparison") — that's interpretation, not observable
- **wrong interpretation:** Structured packs interpretation into `image_type` instead of returning a clean classification
- **layout/positioning errors:** Both treat the comparison as 2 columns instead of 3 (with row label)
- **table extraction errors:** None on cell content — both perfect
- **uncertainty handling problems:** Both runs claim no uncertainty though the muted FOR TEACHERS eyebrow color is a legitimate signal worth flagging
- **formatting/schema problems:** Structured `possible_layout_issues` mixes observation with subjective critique

## 7. Scores

| Dimension | MCP neutral | MCP structured |
|---|---|---|
| OCR/text extraction | 4 (✦ → "+") | 4 (✦ → "+") |
| UI element detection | 5 | 5 |
| layout understanding | 4 | 4 |
| CTA/button detection | 5 | 5 |
| semantic understanding | 5 | 4 (interpretation in image_type) |
| table extraction | 5 | 5 |
| hallucination control | 4 | 3 (subjective layout critique) |
| uncertainty handling | 3 | 3 |
| usefulness for downstream task | 4 | 5 (markdown table is a great handoff) |

## 8. Local recommendations for this screenshot

**What it did well:** Both runs got every cell of the comparison table correct. Structured emitted a clean markdown table — directly usable as input for downstream tooling.

**What it missed:** The ✦ glyph (read as "+"); structured missed `K-8` as a number; structured leaked opinion into the schema.

**Did structured prompting help?** Yes for table extraction — the markdown table format is a strict win. Mixed elsewhere — structured leaked opinion into `image_type` and `possible_layout_issues`.

**What would help:** (1) lock down field semantics — `image_type` should accept a closed enum (`webpage_screenshot`, `mobile_screenshot`, `document`, `chart`, `photo`); (2) move subjective UX critique to a separate optional field clearly labeled `interpretation` so it can be discarded for extraction tasks; (3) explicitly request "include row label column when transcribing tables" to formalize the 3-column structure; (4) ask for a separate `glyphs_and_icons` field so spark/star characters get noted without being merged into prose.
