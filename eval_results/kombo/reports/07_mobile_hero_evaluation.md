# Evaluation Report: 07_mobile_hero.png

## 1. Screenshot metadata
- filename: `07_mobile_hero.png`
- viewport: 390x844
- intended section: top of page (hero), mobile
- actual captured section: mobile nav + hero card with H1 wrapped over 4 lines + subhead wrapped over 4 lines + 3 CTAs on **2 rows** + "No sign-up required"; below the fold, FOR KIDS eyebrow + H2 + start of paragraph (clipped)
- purpose: Mobile headline wrapping, CTA, navigation, readability

## 2. Independent baseline analysis

**Visible text:**
- Top nav: `kombo` (left), `Play`, `Progress` (right pill buttons)
- `READY TO PLAY` (purple eyebrow)
- H1 wrapped over 4 lines: `The math` / `RPG where` / `you build a` / `kingdom`
- Subhead wrapped over 4 lines: `Practice multiplication and` / `division, earn sparks, and grow` / `your kingdom — one kombo at a` / `time.`
- 3 CTAs on **two rows**: row 1 `Start playing` (purple solid) + `I'm a parent` (white outline); row 2 `I'm a teacher` (white outline) by itself
- `No sign-up required`
- `FOR KIDS` (purple eyebrow)
- `Not a test — an adventure` (H2)
- Partial paragraph below (clipped at bottom): "Solve math problems to earn sparks" — rest cut off

**UI elements:** mobile nav, hero card, 3 CTAs in 2 rows, partial FOR KIDS card

**Layout structure:** Single column. CTAs wrap from 1 row (desktop) to 2 rows (mobile) due to width constraint

**Buttons/links:** `Play`, `Progress` (nav); `Start playing`, `I'm a parent`, `I'm a teacher` (hero); none below

**Table content:** none

**Semantic meaning:** Mobile-adapted hero. Text wrapping is heavy because of narrow viewport.

**Uncertainty notes:** The third CTA `I'm a teacher` falling onto its own row could be intentional (cleaner alignment) or could be a soft layout concern (visual asymmetry). Either is plausible.

## 3. MCP neutral output summary

Captured top nav, eyebrow, H1, subhead, 3 CTAs, "No sign-up required", FOR KIDS eyebrow, H2 `Not a test — an adventure`, and partial text "Solve math problems to earn sparks". **Output truncated mid-sentence at "Navigation"** — model hit token limit. Did NOT note CTA wrapping (3 buttons "horizontally aligned" — actually they are on 2 rows). Said the H1 is "centered" — actually left-aligned. Hex color guesses without caveat.

## 4. MCP structured output summary

Schema followed. Captured all visible text. Critically, in `uncertain_or_unreadable_items`, the model **correctly flagged** that the text below FOR KIDS is partially visible/truncated — best uncertainty handling of the dataset so far. `numbers_dates_amounts: not visible` — correct. `table_content: not present` — correct. However, said "Button spacing is appropriate" and "horizontally aligned" — implying single row, which is wrong (CTAs are on 2 rows in mobile).

## 5. Comparison table

| Dimension | Independent baseline | MCP neutral | MCP structured | Notes |
|---|---|---|---|---|
| visible text extraction | All verbatim | Complete up to truncation | Complete | Structured wins (no truncation) |
| UI element detection | nav + hero card + 3 CTAs in 2 rows + partial card | Detected all but flatten CTAs to 1 row | Detected all but flatten CTAs to 1 row | Both miss the row wrap |
| layout understanding | Single col, CTAs wrap to 2 rows | "Buttons horizontally aligned" — wrong | "Button spacing appropriate" — also implies single row | Both wrong |
| CTA/button detection | 3 CTAs identified, primary/secondary | 3 detected, hierarchy correct | 3 detected, hierarchy correct | Match |
| semantic understanding | Mobile-adapted marketing hero | Correct | Correct ("Onboarding screen for a math education app") | Match |
| table extraction | n/a | n/a | n/a | n/a |
| uncertainty handling | Note CTA wrap as design choice | None flagged | **Correctly flagged FOR KIDS body as partial/truncated** | **Structured > neutral on uncertainty** |
| hallucinations | None | Said H1 is "centered" — wrong | Said text alignment in CTAs is "centered" — partially correct (text inside button is centered, but the buttons themselves are left-aligned) | Both have alignment confusion |
| omissions | CTA row wrapping | Output truncated; missed CTA wrap | Missed CTA wrap | Tie on CTA wrap; structured better on truncation |

## 6. Error taxonomy

- **OCR/text errors:** none
- **numeric/date/amount errors:** none
- **omissions:** Neutral truncated mid-output. Both runs missed that the 3 CTAs wrap to 2 rows in this mobile layout — a layout-relevant signal
- **hallucinations:** Neutral claimed H1 is "centered" — actually left-aligned. Both implied CTAs are on a single row
- **wrong interpretation:** Missing the CTA-wrap signal misses a subtle UX consideration
- **layout/positioning errors:** As above
- **table extraction errors:** n/a
- **uncertainty handling problems:** Structured was actually good here (flagged FOR KIDS partial); neutral did not
- **formatting/schema problems:** Neutral truncation is the worst category

## 7. Scores

| Dimension | MCP neutral | MCP structured |
|---|---|---|
| OCR/text extraction | 4 (truncated mid-list) | 5 |
| UI element detection | 4 | 4 |
| layout understanding | 3 (missed CTA wrap, wrong alignment) | 3 (missed CTA wrap) |
| CTA/button detection | 5 (count) but 3 (positions) | 5 (count) but 3 (positions) |
| semantic understanding | 5 | 5 |
| table extraction | n/a | n/a |
| hallucination control | 3 | 4 |
| uncertainty handling | 2 | 5 |
| usefulness for downstream task | 3 (truncation hurts) | 4 |

## 8. Local recommendations for this screenshot

**What it did well:** Structured run is the **best uncertainty handling in the dataset** — it correctly flagged that the FOR KIDS body text is partially visible. Both runs captured the visible text accurately.

**What it missed:** The most layout-significant detail of this screenshot: **the 3 CTAs wrap from 1 row (desktop) to 2 rows (mobile)**. Both runs assert horizontal/single-row CTAs.

**Did structured prompting help?** Yes substantially — it avoided the truncation that plagued neutral, and flagged partial visibility correctly.

**What would help:** (1) explicitly ask the VLM to describe **CTA arrangement** as "1 row × N", "2 rows × N+M", etc. — this surfaces wrap state; (2) reduce token budget pressure on neutral by capping verbose color/typography prose; (3) the structured prompt's `uncertain_or_unreadable_items` field is clearly working — keep it.
