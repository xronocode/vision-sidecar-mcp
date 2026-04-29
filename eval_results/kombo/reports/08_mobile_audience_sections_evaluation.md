# Evaluation Report: 08_mobile_audience_sections.png

## 1. Screenshot metadata
- filename: `08_mobile_audience_sections.png`
- viewport: 390x844
- intended section: audience cards
- actual captured section: full FOR KIDS card + full FOR PARENTS card (with `Join the parent waitlist →` link visible) + most of FOR TEACHERS card (heading + body; teacher waitlist link below fold)
- purpose: Mobile vertical stacking of audience cards

## 2. Independent baseline analysis

**Visible text (preserving line wraps as displayed):**
- `FOR KIDS` (**purple** eyebrow)
  - `Not a test — an adventure`
  - "Solve math problems to earn sparks. Use sparks to build your kingdom. Each correct answer makes your world bigger." — wraps to 4 mobile lines but is **2 sentences total**
- `FOR PARENTS` (**purple** eyebrow)
  - `Math practice without the nagging` (H2 wraps to 2 lines: "Math practice without the" / "nagging")
  - "A parent dashboard is on the way. See progress, set goals, and stay informed — without turning into homework police."
  - `Join the parent waitlist →` (purple link)
- `FOR TEACHERS` (**grey/muted** eyebrow — consistent with desktop and tablet screenshots)
  - `Zero prep, full visibility`
  - "Classroom tools are on the roadmap. Assign practice, track mastery, and spot who needs help — all from one dashboard."
  - (`Join the teacher waitlist →` link is below the visible fold)

**UI elements:** 3 audience cards stacked vertically; 1 inline link visible (parent waitlist)

**Layout structure:** Mobile single-column, full-width cards

**Buttons/links:** `Join the parent waitlist →`

**Table content:** none

**Semantic meaning:** Same persona-segmented section, mobile-adapted

**Uncertainty notes:** Teacher waitlist link below fold (cannot confirm or deny presence from this screenshot alone, though context suggests it exists). Muted FOR TEACHERS eyebrow consistent with prior screenshots.

## 3. MCP neutral output summary

Captured all visible text. Reproduced wrapped lines with newlines inserted, treating line wraps as if they were paragraph breaks (rendered as multi-line block-quote text). **Asserted all three eyebrows are purple** — wrong for FOR TEACHERS. Correctly noted no teacher waitlist link visible (since it's below fold). No truncation. "All visible text is legible" — overconfident on color.

## 4. MCP structured output summary

`visible_text_exactly_as_seen` field is **mostly correct but introduced a sentence break**: in FOR KIDS, listed as separate items "Solve math problems to earn sparks." (with period) and "Use sparks to build your kingdom. Each correct answer makes your world bigger." — in fact the first line ends with sparks. but it is one continuous sentence; the line-wrap-induced visual break does not correspond to a sentence break in the source text. So this is treating line wrap as logical structure, which is an OCR-segmentation error. Same FOR TEACHERS color hallucination. `numbers_dates_amounts: not visible`, `table_content: not present` — both correct. `uncertain_or_unreadable_items: None visible` — overconfident.

## 5. Comparison table

| Dimension | Independent baseline | MCP neutral | MCP structured | Notes |
|---|---|---|---|---|
| visible text extraction | All verbatim (3 sentences across all bodies) | Inserted line breaks but content correct | **Split FOR KIDS body across two list items** as if 2 paragraphs (treating mobile line wrap as sentence break) | Structured introduces a subtle structural error |
| UI element detection | 3 cards + 1 link | Same | Same | Match |
| layout understanding | Vertical stack, mobile | Correct | Correct | Match |
| CTA/button detection | 1 link | 1 link | 1 link | Match |
| semantic understanding | Persona segmentation | Correct | Correct | Match |
| table extraction | n/a | n/a | n/a | n/a |
| uncertainty handling | Note teacher link below fold + muted color | Did not note below-fold absence; "no uncertainty" | Did not note below-fold absence; "None" | Both miss below-fold inference |
| hallucinations | None | All-purple eyebrow assertion | All-purple eyebrow assertion | Stable hallucination |
| omissions | None | None (link absence not flagged but not extracted either) | None (same) | Match |

## 6. Error taxonomy

- **OCR/text errors:** Structured introduced a line-wrap-induced sentence split for FOR KIDS body
- **numeric/date/amount errors:** n/a
- **omissions:** Both runs failed to note that the FOR TEACHERS waitlist link should exist (consistent with the section structure) but is below the visible fold — would be useful inference for downstream
- **hallucinations:** All three eyebrows declared purple. FOR TEACHERS is grey
- **wrong interpretation:** Same systemic issue as 02 and 06
- **layout/positioning errors:** none significant
- **table extraction errors:** n/a
- **uncertainty handling problems:** "no uncertainty" claim despite a missing element (teacher waitlist link)
- **formatting/schema problems:** Structured's tendency to use mobile line wraps as logical separators

## 7. Scores

| Dimension | MCP neutral | MCP structured |
|---|---|---|
| OCR/text extraction | 5 | 4 (FOR KIDS sentence split) |
| UI element detection | 5 | 5 |
| layout understanding | 5 | 5 |
| CTA/button detection | 5 | 5 |
| semantic understanding | 4 | 4 |
| table extraction | n/a | n/a |
| hallucination control | 3 (color) | 3 (color) |
| uncertainty handling | 3 | 3 |
| usefulness for downstream task | 4 | 4 |

## 8. Local recommendations for this screenshot

**What it did well:** Both runs captured every word of visible text. Both correctly omitted the teacher waitlist link from extraction (it's below fold).

**What it missed:** Same color hallucination as 02 and 06. Structured introduced a phantom sentence break in FOR KIDS body where the actual source has a single sentence wrapping mid-line.

**Did structured prompting help?** No on this image. Structured got slightly worse OCR (sentence split). Both equally weak on color uncertainty.

**What would help:** (1) explicit instruction to **preserve sentences as written** ignoring visual line wraps — "join consecutive lines that share a paragraph block; only break on a blank line or new heading"; (2) per-element color attribute (already noted in 06's recommendation); (3) for `uncertain_or_unreadable_items`, prompt the model to also list "expected elements that may be below the fold" — gives downstream a hint to scroll.
