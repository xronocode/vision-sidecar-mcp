# Evaluation Report: 10_small_mobile_stress.png

## 1. Screenshot metadata
- filename: `10_small_mobile_stress.png`
- viewport: 320x568
- intended section: top of page (small-mobile stress test)
- actual captured section: top nav + READY TO PLAY eyebrow + H1 wrapped over **5 lines** + subhead wrapped over 4 lines. **CTAs and "No sign-up required" are below the fold (clipped).** No FOR KIDS section visible — page barely shows the hero.
- purpose: Small mobile stress test, clipping, CTA readability, layout robustness

## 2. Independent baseline analysis

**Visible text:**
- Top nav: `kombo` (left), `Play`, `Progress` (right pills, partially overlapping the right edge — they fit but tightly)
- `READY TO PLAY` (purple eyebrow)
- H1 wrapped over **5 lines**: `The math` / `RPG` / `where you` / `build a` / `kingdom`
- Subhead wrapped over 4 lines: `Practice multiplication and` / `division, earn sparks, and` / `grow your kingdom — one` / `kombo at a time.`

**Below the fold (NOT visible in this screenshot):** the 3 CTAs (`Start playing`, `I'm a parent`, `I'm a teacher`), `No sign-up required`, FOR KIDS card, and everything else. The hero CTAs are entirely clipped at this viewport.

**Text alignment within the card:** **left-aligned** (eyebrow, H1, and subhead are all flush-left within the card, not centered). This is observable from the consistent left edge of `READY TO PLAY`, the `T` of `The math`, and `Practice` in the subhead.

**UI elements:** mobile nav (logo + 2 pill buttons); hero card with eyebrow + H1 + subhead (clipped before CTAs)

**Layout structure:** Single column. Heavy text wrapping. CTAs entirely clipped.

**Buttons/links:** only `Play`, `Progress` (nav); **no hero CTAs visible**

**Table content:** none

**Numbers visible:** none

**Semantic meaning:** Same hero, but at a viewport so narrow that primary CTAs are not visible above the fold — a real readability/UX concern at this size.

**Uncertainty notes:** Whether `Start playing` and the persona CTAs exist for this viewport cannot be confirmed from this image alone (they are below fold). But the absence is itself the signal — at 320×568, the hero is not actionable without scrolling.

## 3. MCP neutral output summary

Captured top nav, eyebrow, H1, subhead. **Failed to note any clipping or below-fold content.** Asserted text is "centered horizontally" — **wrong** (left-aligned). Implied the layout is normal/standard. No mention of the 5-line H1 wrap as a stress signal. Output stops cleanly without truncation.

## 4. MCP structured output summary

Schema followed cleanly. Captured the same visible text. **`buttons_and_links` field reports only the nav buttons** (`Play`, `Progress`) — technically correct since the hero CTAs are below fold. However, `numbers_dates_amounts: Not visible` — correct. `table_content_if_present: Not present` — correct. `uncertain_or_unreadable_items: None` — **wrong**, given that the user's CTAs are unmistakably below fold (the page is mid-content with no indication of completion). `possible_layout_issues: None observed` — **wrong**, given the H1 wraps over 5 lines and the entire CTA region is clipped. Asserted "All text within the white card is centered" — wrong (left-aligned).

## 5. Comparison table

| Dimension | Independent baseline | MCP neutral | MCP structured | Notes |
|---|---|---|---|---|
| visible text extraction | All visible verbatim | Complete | Complete | Match |
| UI element detection | nav + hero card with clipped CTA region | Detected nav + card; no clipping flag | Detected nav + card; no clipping flag | Both miss clipping |
| layout understanding | Single col, heavy wrap, CTAs clipped | "Clean, centered" — wrong on both alignment and completeness | "Clean, centered" — wrong on both alignment and completeness | Both wrong |
| CTA/button detection | Only nav buttons visible | Only nav buttons | Only nav buttons | Match (correct given visible content) |
| semantic understanding | Hero (truncated) of marketing page | Said it's an "introductory interface" | Said it's an "introductory interface for a math-focused RPG" | Match. Inferred Play/Progress are navigation buttons (reasonable) |
| table extraction | n/a | n/a | n/a | n/a |
| uncertainty handling | Note CTAs below fold; H1 5-line wrap is a stress signal | "No uncertainties" | "None" | Both fail |
| hallucinations | None | "Centered" alignment claim | "Centered" alignment claim | Both wrong |
| omissions | CTAs are below fold → relevant for downstream | Did not flag missing CTAs | Did not flag missing CTAs (despite hero context strongly implying their existence elsewhere) | Both omit a useful inference |

## 6. Error taxonomy

- **OCR/text errors:** none
- **numeric/date/amount errors:** none
- **omissions:** Both runs failed to flag that the hero's primary CTAs are below the visible fold — the central UX observation for a 320×568 stress test
- **hallucinations:** Both runs claim text is "centered horizontally" — actually left-aligned within the card
- **wrong interpretation:** Both runs treat this as a complete, well-laid-out screen — missing that this is a clipped/incomplete view of a longer hero
- **layout/positioning errors:** Centered claim is the chief positioning error
- **table extraction errors:** n/a
- **uncertainty handling problems:** This is the worst-case dataset failure: the entire purpose of the stress screenshot was to see if the model recognizes clipping/overflow signals, and **both runs returned "no issues observed"**
- **formatting/schema problems:** none

## 7. Scores

| Dimension | MCP neutral | MCP structured |
|---|---|---|
| OCR/text extraction | 5 | 5 |
| UI element detection | 4 | 4 |
| layout understanding | 2 (missed clipping, wrong alignment) | 2 (same) |
| CTA/button detection | 5 (correct on what's visible) | 5 |
| semantic understanding | 4 | 4 |
| table extraction | n/a | n/a |
| hallucination control | 3 (centered claim) | 3 (centered claim) |
| uncertainty handling | 1 (asserted no uncertainty in a clearly clipped view) | 1 (same) |
| usefulness for downstream task | 2 (downstream would not know to scroll) | 2 (same) |

## 8. Local recommendations for this screenshot

**What it did well:** Read every visible character perfectly.

**What it missed:** Everything that made this image a stress test: (1) the H1 wrapping over 5 lines as a small-viewport signal; (2) the entire CTA region being below the fold; (3) the `No sign-up required` line being clipped. Neither run flagged any of these.

**Did structured prompting help?** No. Both runs returned essentially the same output and made the same blind assertions ("centered", "no issues").

**What would help:** (1) inject a viewport-aware question into the prompt: "estimate whether the page continues below the bottom edge — would you expect more content?" — model can answer "yes" based on incomplete content patterns; (2) explicit alignment description discipline ("for each text block, state alignment as left/center/right based on x-position within its container"); (3) **a viewport-mode for the MCP server**: a separate tool `analyze_mobile_screenshot` that prepends a system prompt "this is a small viewport screenshot — pay attention to clipping, text wrapping, and below-fold content"; (4) prompting that **asks the model to enumerate things absent that would normally appear** — the inverse-extraction prompt; (5) consider tiling: cap height-to-width ratio and warn when content density suggests overflow.
