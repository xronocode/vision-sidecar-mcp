# Evaluation Report: 01_desktop_hero.png

## 1. Screenshot metadata
- filename: `01_desktop_hero.png`
- viewport: 1440x900
- intended section: top of page (hero)
- actual captured section: hero card with READY TO PLAY eyebrow + H1 + subhead + 3 CTAs + "No sign-up required"; below the fold the FOR KIDS card and start of FOR PARENTS are visible
- purpose: Hero section, main headline, navigation, CTA, visual hierarchy

## 2. Independent baseline analysis

**Visible text (left-to-right, top-to-bottom):**
- Top nav: `kombo` (left), `Play`, `Progress` (right, pill buttons)
- Inside main card:
  - `READY TO PLAY` (purple, uppercase, tracked-out eyebrow)
  - `The math RPG where you build a kingdom` (H1, dark, wraps over 2 lines)
  - `Practice multiplication and division, earn sparks, and grow your kingdom — one kombo at a time.` (subhead, 2 lines, mid-grey)
  - 3 CTAs in a row: `Start playing` (purple solid), `I'm a parent` (white outline), `I'm a teacher` (white outline)
  - `No sign-up required` (small, muted)
- A purple egg-shaped illustration to the right of the headline
- Below the white inner card: `FOR KIDS` eyebrow + H2 `Not a test — an adventure` + paragraph "Solve math problems to earn sparks. Use sparks to build your kingdom. Each correct answer makes your world bigger."
- Bottom of viewport: `FOR PARENTS` eyebrow + start of H2 `Math practice without the nagging`

**UI elements:** top nav, hero card (rounded), 3 CTAs, decorative egg illustration, two audience cards (FOR KIDS visible in full, FOR PARENTS clipped)

**Layout structure:** Two-column inside the hero (left text block + right illustration); single-column stacked sections below

**Buttons/links:** `Play`, `Progress` (nav), `Start playing` (primary), `I'm a parent`, `I'm a teacher` (secondary)

**Table content:** none

**Semantic meaning:** Marketing landing page for an educational math RPG (kombo); persona-segmented messaging starts immediately below the fold

**Uncertainty notes:** None significant. The egg illustration is unmistakable; text is sharp.

## 3. MCP neutral output summary

The neutral output captured: top nav (`kombo`/`Play`/`Progress`), the READY TO PLAY eyebrow, H1, subhead, all three CTAs, "No sign-up required". It correctly identified `FOR KIDS` with full description and started `FOR PARENTS` heading. **Output was truncated mid-sentence at "Math practice without the nagging" (`** — the model ran out of output tokens before completing the description. Identified the purple oval illustration. Made unverified hex-color guesses for the background/labels but flagged them as not confirmed.

## 4. MCP structured output summary

Structured output extracted text faithfully and flagged the FOR PARENTS section as "partially cut off" — accurate. Correctly classified Start playing as primary, others as secondary. Did NOT mention the purple egg illustration in `key_ui_elements` (it was mentioned only in passing under "Visual elements"). `numbers_dates_amounts: Not visible` — correct. `table_content: Not present` — correct. Followed the schema cleanly with no skipped fields. Better completion than neutral — did not truncate.

## 5. Comparison table

| Dimension | Independent baseline | MCP neutral | MCP structured | Notes |
|---|---|---|---|---|
| visible text extraction | All visible text captured verbatim | All visible text captured up to truncation point; missed FOR PARENTS body | All visible text captured; correctly noted FOR PARENTS partially cut off | Structured > neutral due to neutral truncation |
| UI element detection | Nav + 3 CTAs + 2 cards + egg illustration | Same set, plus correct color cues | Same set; egg illustration mentioned only under "Visual elements", weakly | Both detected the egg, structured underweights it |
| layout understanding | 2-col hero (text+image) + stacked sections | Described as "single white card with sections" — missed the 2-column hero subdivision | Described as "single-column" — also missed the 2-column hero | Both miss the hero's text+illustration two-column split |
| CTA/button detection | 3 hero CTAs + 2 nav buttons | All identified, primary/secondary distinguished | All identified, primary/secondary distinguished | Match |
| semantic understanding | Edu-RPG marketing page, persona-segmented | Correct | Correct | Match |
| table extraction | n/a | n/a | n/a (correctly stated not present) | n/a |
| uncertainty handling | None flagged | Hex codes flagged as "not confirmed" — good | Correctly flagged FOR PARENTS truncation | Structured is sharper |
| hallucinations | None | Mild: hex color guesses (caveated), claimed sections "centered horizontally" which is wrong (text is left-aligned) | Mild: claimed alignment is "centered horizontally" — wrong (left-aligned) | Both inject false alignment claim |
| omissions | None | Truncated body of FOR PARENTS (output truncation) | None significant | Neutral has hard omission via truncation |

## 6. Error taxonomy

- **OCR/text errors:** none
- **numeric/date/amount errors:** n/a
- **omissions:** Neutral truncated mid-output and missed FOR PARENTS body
- **hallucinations:** Both runs claim text is "centered horizontally" — actually left-aligned within the card
- **wrong interpretation:** Both miss the 2-column hero subdivision (text on left, egg illustration on right)
- **layout/positioning errors:** as above; alignment claim is wrong
- **table extraction errors:** n/a
- **uncertainty handling problems:** Neutral made hex-color guesses (caveated). Structured missed flagging the alignment as "uncertain" — instead asserted it
- **formatting/schema problems:** Structured followed schema cleanly. Neutral's heavy markdown-formatted output is verbose

## 7. Scores

| Dimension | MCP neutral | MCP structured |
|---|---|---|
| OCR/text extraction | 3 (truncated) | 5 |
| UI element detection | 4 | 4 |
| layout understanding | 3 (missed 2-col hero) | 3 (missed 2-col hero) |
| CTA/button detection | 5 | 5 |
| semantic understanding | 5 | 5 |
| table extraction | n/a | n/a |
| hallucination control | 3 (alignment claim, hex guesses) | 4 (alignment claim) |
| uncertainty handling | 3 | 4 |
| usefulness for downstream task | 3 (truncation hurts) | 4 |

## 8. Local recommendations for this screenshot

**What it did well:** Read every word of visible text at high fidelity. Correctly identified primary vs. secondary CTA hierarchy and the persona-segmented page structure.

**What it missed:** The two-column nature of the hero (text + illustration); both runs flattened it to "single column with sections". Both asserted text is "centered" when it is left-aligned within the card.

**Did structured prompting help?** Yes — neutral truncated and lost FOR PARENTS body; structured fit within the token budget. Structured also correctly flagged the partial visibility.

**What would help:** (1) higher max output tokens to prevent neutral truncation; (2) explicit instruction to describe alignment by quadrant (top-left / centered) rather than guessing; (3) ask the VLM to enumerate distinct visual regions (text block, image block) before describing them, which would catch the 2-col hero structure.
