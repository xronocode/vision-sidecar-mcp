# Evaluation Report: 04_desktop_comparison_table.png

## 1. Screenshot metadata
- filename: `04_desktop_comparison_table.png`
- viewport: 1440x900
- intended section: comparison table (WHY KOMBO)
- actual captured section: **byte-identical to 03_desktop_how_it_works.png** (MD5 a444572cb759b0b68bebcf7a8bec8958). Page bottoms out at maxScroll=973; no separate scroll position exists at this viewport that frames the table without HOW IT WORKS above
- purpose: Table OCR, row/column extraction, comparison logic
- **note:** This pair of runs serves as a run-to-run consistency check because the input pixels are identical to screenshot 03. The VLM is non-deterministic (sampling temperature > 0), so output differences here are pure model variance rather than image variance.

## 2. Independent baseline analysis

Identical to report 03. Highlights specific to the table:

**Comparison table content:**

| (row label) | kombo | Prodigy |
|---|---|---|
| Scope | Focused on math facts | Full curriculum K-8 |
| Core skill | Speed and retention | Conceptual understanding |
| Complexity | Start in 5 seconds | Setup and onboarding |
| Philosophy | Free, no ads, no paywalls | Freemium with membership |

**Numbers visible:** `5` (in "5 seconds"), `K-8` (in "K-8")

**Buttons/links:** `Join the parent waitlist →`, `Join the teacher waitlist →`

**Uncertainty:** FOR TEACHERS eyebrow appears in muted grey vs. purple eyebrows on the other sections.

## 3. MCP neutral output summary

Cleaner than 03 neutral — no truncation. Captured all sections (`Top Header` / `FOR TEACHERS` / `HOW IT WORKS` / `WHY KOMBO`). Reproduced the comparison table in a markdown table (4 rows × 2 cols, with row label column included this time). Same OCR errors: `Earn + Sparks` instead of `Earn ✦ Sparks`. Did NOT note the FOR TEACHERS eyebrow color (called the section header "dark gray" — partially correct).

## 4. MCP structured output summary

Best structured output of the dataset. `numbers_dates_amounts` correctly captured **both** `5 seconds` AND `K-8` (run 03 structured missed `K-8`). Markdown table is complete. `possible_layout_issues` is empty / "None observed" — refrained from injecting subjective critique that 03 structured did. `image_type` field returned the clean value "UI screenshot" (vs. 03's verbose interpretation). This run shows the model can produce clean schematic output when sampling lands well.

## 5. Comparison table

| Dimension | Independent baseline | MCP neutral | MCP structured | Notes |
|---|---|---|---|---|
| visible text extraction | All visible verbatim | Complete (✦ → "+") | Complete (✦ → "+") | Tie |
| UI element detection | Card + 4 step cards + table + 2 links | All present | All present | Match |
| layout understanding | Sections stacked; 4-col cards; 3-col table | Stacked; horizontal cards; 2-col table (row labels merged into prose) | Stacked; horizontal cards; markdown table includes row labels as first col | **Structured 04 superior to neutral on table column count** |
| CTA/button detection | 2 inline links | 2 links | 2 links | Match |
| semantic understanding | Brand comparison | Correct | Correct, clean image_type | Structured 04 cleaner than 03 |
| table extraction | 4 rows × 3 cols | Cells correct, structure 2-col + row labels mentioned in body | Cells correct, full 3-col markdown table | Structured wins |
| uncertainty handling | Note FOR TEACHERS muted color | None flagged | None flagged | Both miss it |
| hallucinations | None | None substantive | None — refrained from subjective critique unlike 03 structured | Structured 04 cleaner |
| omissions | None | None | None (caught both `5 seconds` AND `K-8`) | Best run on numbers field |

**Run-to-run consistency note (pixels identical to screenshot 03):**
- ✦ glyph misread is **stable** (same error in 03 and 04 across both prompts)
- Cell content extraction is **stable** (4×2 cells correct in all 4 runs)
- `numbers_dates_amounts` is **unstable** (03 structured: `5 seconds` only; 04 structured: `5 seconds` AND `K-8`)
- `image_type` field content is **unstable** (03 structured: long sentence; 04 structured: clean "UI screenshot")
- `possible_layout_issues` is **unstable** (03 structured: subjective critique; 04 structured: "None observed")
- This is meaningful: critical OCR errors persist across runs (likely model limitation), but small-field outputs vary substantially (likely sampling).

## 6. Error taxonomy

- **OCR/text errors:** ✦ → `+` (stable across runs)
- **numeric/date/amount errors:** caught both numbers in this run (improvement over 03)
- **omissions:** none significant
- **hallucinations:** none in this run (improvement over 03 structured)
- **wrong interpretation:** none
- **layout/positioning errors:** neutral describes table as 2-col instead of 3-col (with row labels)
- **table extraction errors:** none on cell content
- **uncertainty handling problems:** still missed muted FOR TEACHERS eyebrow color
- **formatting/schema problems:** none

## 7. Scores

| Dimension | MCP neutral | MCP structured |
|---|---|---|
| OCR/text extraction | 4 (✦ → "+") | 4 (✦ → "+") |
| UI element detection | 5 | 5 |
| layout understanding | 4 | 5 (correctly counts row label column) |
| CTA/button detection | 5 | 5 |
| semantic understanding | 5 | 5 |
| table extraction | 4 | 5 (clean markdown w/ row labels) |
| hallucination control | 5 | 5 |
| uncertainty handling | 3 | 3 |
| usefulness for downstream task | 4 | 5 |

## 8. Local recommendations for this screenshot

**What it did well:** Best structured run of the dataset — clean schema, complete numbers field, no subjective leakage, full markdown table.

**What it missed:** ✦ → "+" persists. Muted FOR TEACHERS eyebrow color still not flagged.

**Did structured prompting help?** Yes — the structured run was clearly more useful for downstream consumption than the neutral run on this image.

**What would help:** (1) prompt-level constraint on `image_type` (closed enum); (2) specify row-label column should be enumerated; (3) glyph callout to break ✦ → "+" pattern; (4) since the 03 vs 04 comparison shows the same image yields different structured outputs, **temperature should be lowered** at the MCP server level for extraction tasks (currently the VLM appears to be using its default sampling temperature). Lower temperature would also reduce subjective leakage.
