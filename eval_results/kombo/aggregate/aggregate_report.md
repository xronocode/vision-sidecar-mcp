# Aggregate MCP Vision Evaluation Report — kombo website

**Evaluator setup**
- Local VLM: `qwen3-vl:8b` served via Ollama at `http://INTERNAL-HOST:11434`
- MCP server: `vision-sidecar-mcp` (this repo) using `analyze_image` tool
- Screenshot capture: Playwright MCP (`@playwright/mcp`)
- Dataset: 10 screenshots of `https://kombo-41e.pages.dev/` across viewports 320×568 → 1440×900
- Prompts evaluated: a neutral "describe accurately" prompt and a structured 10-section auditor prompt
- Total VLM calls: 20 (10 per prompt). Note: screenshots 03 and 04 are byte-identical (page is too short at 1440×900 to scroll between "How it works" and the comparison table); the 04 run pair therefore acts as a free run-to-run consistency check on identical pixels.

---

## 1. Executive summary

`qwen3-vl:8b` is **a competent OCR layer** for marketing-page screenshots: it reproduces visible English body text with high fidelity and preserves structured table cells reliably. Where it fails, it fails systematically — and the failures matter for an extraction product:

- **Recurring OCR error on a single brand glyph**: the spark symbol `✦` was read as `+` in **all 5 screenshots that show it**, across both prompts. This is a stable model-level error that prompt changes did not fix.
- **Color hallucination**: in 4 screenshots the FOR TEACHERS eyebrow is rendered in a muted grey to signal "on the roadmap" status; the model called it purple in **every run** that included it. The model paints by inferred role (label = colored eyebrow), not by observed pixels.
- **Overconfident uncertainty handling**: the dataset's hardest screenshot (320×568 small-mobile stress) has **CTAs entirely below the fold** and an H1 wrapping over 5 lines. Both runs returned `uncertainty: none` and `layout issues: none observed`. The single screenshot specifically designed to catch overflow/clipping was the dataset's worst-served by the model.
- **Comparison-table extraction is the model's strongest skill**: every cell, including narrow wrapped mobile cells, was transcribed correctly across all 6 table-containing runs. This is production-quality for static-table OCR.
- **Structured prompting helps for downstream consumption** (markdown tables, explicit numbers field, clearer structure) and **avoids the truncation issues** that hit the neutral prompt twice (screenshots 01 and 07). It introduces a different problem: opinion leaks into `image_type` and `possible_layout_issues`.
- **Verdict**: pilot-ready as a private extraction layer, with non-trivial prompt and schema work to harden it before production.

---

## 2. Dataset overview

| filename | viewport | section | purpose |
|---|---|---|---|
| 01_desktop_hero.png | 1440×900 | top of page (hero) | Hero section, headline, navigation, CTA, visual hierarchy |
| 02_desktop_audience_sections.png | 1440×900 | FOR KIDS / FOR PARENTS / FOR TEACHERS cards | Audience cards, section structure, text extraction |
| 03_desktop_how_it_works.png | 1440×900 | HOW IT WORKS step cards (also catches WHY KOMBO due to short page) | Step sequence, icons, process interpretation |
| 04_desktop_comparison_table.png | 1440×900 | WHY KOMBO comparison table (byte-identical to 03 — page is too short to scroll past) | Table OCR, row/column extraction, comparison logic |
| 05_tablet_portrait_hero.png | 768×1024 | top (tablet portrait) | Tablet portrait hero layout, CTA visibility, text wrapping |
| 06_tablet_landscape_sections.png | 1024×768 | audience cards (tablet landscape) | Intermediate responsive layout |
| 07_mobile_hero.png | 390×844 | top (mobile) | Mobile headline wrapping, CTA, navigation |
| 08_mobile_audience_sections.png | 390×844 | audience cards (mobile) | Mobile vertical stacking |
| 09_mobile_comparison_table.png | 390×844 | step cards + comparison table (mobile) | Mobile table behavior, OCR stress |
| 10_small_mobile_stress.png | 320×568 | top (small-mobile stress) | Clipping, CTA readability, layout robustness |

---

## 3. Average scores

Scoring: 0–5 (5 = production-usable; 3 = needs human review; 0 = unusable). Scores are pulled from the 10 per-screenshot evaluation reports.

### 3.1 MCP neutral average by dimension

| Dimension | n | Mean (out of 5) |
|---|---:|---:|
| OCR/text extraction | 10 | 4.3 |
| UI element detection | 10 | 4.7 |
| layout understanding | 10 | 3.8 |
| CTA/button detection | 10 | 5.0 |
| semantic understanding | 10 | 4.6 |
| table extraction (where applicable) | 3 | 4.7 |
| hallucination control | 10 | 3.6 |
| uncertainty handling | 10 | 2.7 |
| usefulness for downstream task | 10 | 3.6 |

### 3.2 MCP structured average by dimension

| Dimension | n | Mean (out of 5) |
|---|---:|---:|
| OCR/text extraction | 10 | 4.5 |
| UI element detection | 10 | 4.7 |
| layout understanding | 10 | 4.0 |
| CTA/button detection | 10 | 5.0 |
| semantic understanding | 10 | 4.3 |
| table extraction (where applicable) | 3 | 5.0 |
| hallucination control | 10 | 3.5 |
| uncertainty handling | 10 | 3.1 |
| usefulness for downstream task | 10 | 4.3 |

### 3.3 Structured vs. neutral delta (structured − neutral)

| Dimension | Δ |
|---|---:|
| OCR/text extraction | +0.2 |
| UI element detection | 0.0 |
| layout understanding | +0.2 |
| CTA/button detection | 0.0 |
| semantic understanding | **−0.3** |
| table extraction | **+0.3** |
| hallucination control | −0.1 |
| uncertainty handling | **+0.4** |
| usefulness for downstream task | **+0.7** |

**Interpretation**: structured prompting yields a clear win on `usefulness` (downstream-machine-readability), `table extraction`, and `uncertainty handling`. It is roughly tied on most dimensions and slightly worse on `semantic understanding` due to opinion leaking into the `image_type` and `possible_layout_issues` fields.

---

## 4. Best and worst cases

- **Best-performing screenshot (per total scores)**: **04_desktop_comparison_table.png** (structured run). Clean schema, both numbers caught (`5 seconds` and `K-8`), full markdown table with row labels, no subjective leakage. Total score 9 of 9 dimensions ≥ 5 except OCR (4 due to ✦) and uncertainty (3).
- **Worst-performing screenshot**: **10_small_mobile_stress.png** (both runs equally weak). Both asserted "no uncertainty" / "no layout issues" on a screenshot whose entire purpose was catching clipping and overflow. Uncertainty score 1/5 in both runs.
- **Easiest category**: **comparison-table OCR**. Across screenshots 03, 04, and 09 (mobile), every cell transcribed correctly in all 6 runs (3 screenshots × 2 prompts). Cell text wrapping in narrow columns did not break extraction.
- **Hardest category**: **small/clipped viewport interpretation**. The model gives no signal that content extends beyond the visible frame, even when the visible content is structurally incomplete (e.g. a hero with no CTAs visible).

---

## 5. Common failure modes

| Failure mode | Occurrences in dataset | Notes |
|---|---|---|
| `Earn ✦ Sparks` read as `Earn + Sparks` | 5 / 5 screenshots that show it (02, 03, 04, 09 — and indirectly 06's body refs); both prompts; **stable** | Same model, same wrong character every time. Can't be fixed by prompting alone — needs explicit glyph-callout instruction or a downstream find/replace pass. |
| FOR TEACHERS eyebrow color asserted as purple | 4 / 4 screenshots that show it (02, 03, 06, 08); both prompts | The eyebrow is muted grey because the section is "on the roadmap". The model paints colors by role, not by pixels. |
| Below-fold content not flagged | screenshots 07 and 10 | Especially severe in 10 (CTAs entirely below fold). Structured run on 07 *did* flag partial visibility — the only correct uncertainty handling on this dimension. |
| Output truncation | screenshots 01 (neutral) and 07 (neutral) | Neutral prompt's verbose color/typography prose burns the output token budget. Structured prompt did not truncate on any screenshot. |
| Two-column hero subdivision flattened to "single column with sections" | screenshot 01 | Both runs missed that desktop hero is a 2-col layout (text + egg illustration). |
| Subjective critique injected into observation field | screenshots 03 and 09 (structured) | "Complexity is not a standard metric for app comparison" — opinion in `possible_layout_issues`. Schema doesn't separate observation from interpretation. |
| Text alignment claimed as "centered" when actually left-aligned | screenshots 01, 07, 10 | Recurring positioning error — model defaults to "centered" when description is unclear. |
| `image_type` field bloated with semantic sentences | screenshots 03, 05 (structured) | Should be a closed enum classification, currently free text. |
| Mobile line wrap treated as logical sentence break | screenshot 08 (structured) | Splits a single sentence into two list items based on wrap. |
| Hex color codes asserted without caveat | screenshots 02, 05, 06 (neutral) | Model invents specific hex codes that have no observation basis. |
| Mobile CTA wrap (1 row → 2 rows) missed | screenshot 07 | Both runs claim CTAs are "horizontally aligned" — actually wrapped. |

---

## 6. Prompt comparison: neutral vs. structured

| Comparison | Outcome |
|---|---|
| Where structured improved output | Table extraction (markdown format with row labels, +0.3 avg). Numbers field surfaced explicitly. Uncertainty section forces the model to consider partial visibility — best-in-class on screenshot 07's structured run. Avoids token-budget truncation that hit neutral on screenshots 01 and 07. |
| Where structured did not help | OCR errors (`✦ → +`) and color hallucinations (FOR TEACHERS eyebrow) are stable across both prompts — model-level, not prompt-level. |
| Did structured reduce hallucinations? | **Slightly worse on hallucination control** (−0.1 avg) because the explicit `image_type` and `possible_layout_issues` fields **invite opinion leakage**. Neutral has no such fields and so cannot leak there. |
| Did structured improve extraction completeness? | Yes for tables and numbers. Roughly equal for prose body text. |
| Did structured cause verbosity without accuracy gain? | No. Structured output is consistently more compact than neutral and never truncated in this dataset. The opposite is true: **neutral runs are verbose and get truncated**. |

---

## 7. Recommended MCP system prompt

The current server appears to forward the user prompt directly to the VLM. A baseline system prompt added at the server level would harden behavior across all callers:

```
You are an extraction-only vision agent for UI and document screenshots.

PRINCIPLES (in priority order):
1. Extraction over interpretation. Report what is visible, not what you infer.
2. No invention. If you cannot read it, say so. Never fill in missing words, hex codes,
   or alignments based on what is "probably" there.
3. Calibrated uncertainty. Mark anything you are not certain about. Volunteer when an
   element appears clipped, partially visible, or below the fold.
4. Per-element attribution. When describing color, weight, or alignment, attach the
   description to a single element. Do not generalize across multiple elements
   ("all eyebrows are purple") — describe each one separately.
5. Pixel-accurate text. Preserve exact spelling, case, punctuation, glyphs, and
   numbers. Distinguish punctuation from icon characters: ‣ + ✦ ✕ → ↗ etc. are
   visually distinct from the operators they resemble.
6. Structure preservation. Mobile line wraps inside a paragraph are NOT sentence
   breaks. Join wrapped lines unless separated by a blank line or new heading.
7. No subjective critique. Do not call layouts "clean", "intuitive", or "well-designed".
   Do not suggest UX improvements. Report observations only.

OUTPUT POLICY:
- For colors, use qualitative descriptors (light purple, muted grey, white, dark grey).
  Never invent hex codes.
- For alignment, state left/center/right relative to the containing element, only when
  determinable from observed x-positions.
- For tables, transcribe row-label column when present; report row count × column count.
- For viewport screenshots, end every output with one of:
    visible_content_complete: true
    visible_content_complete: false (and list what appears clipped)

Return only the requested fields. Do not add commentary outside the schema.
```

---

## 8. Recommended MCP tool response schema

Move the current free-text response toward a structured JSON schema. Below is a proposed JSON shape; the `analyze_image` tool would still accept a custom prompt but the **server enforces the schema** and validates fields before returning.

```jsonc
{
  // closed enum
  "image_type": "webpage_screenshot" | "mobile_screenshot" | "document" | "diagram" | "chart" | "photo" | "ui_mockup" | "other",
  "viewport_class": "desktop" | "tablet" | "mobile" | "small_mobile" | "unknown",

  // raw text faithfully reconstructed
  "visible_text": [
    {
      "block_id": "string",     // stable per-block id
      "role": "heading_h1" | "heading_h2" | "heading_h3" | "eyebrow" | "body" | "label" | "button_label" | "link_text" | "table_cell" | "caption" | "nav",
      "text": "string",         // wraps joined into one string
      "x_position": "left" | "center" | "right" | "unknown",
      "color_descriptor": "purple" | "grey_muted" | "black" | "white" | "..." | "unknown",
      "weight": "bold" | "regular" | "light" | "unknown"
    }
  ],

  "key_ui_elements": [{ "kind": "card" | "button" | "link" | "image" | "table" | "input" | "...", "label": "...", "notes": "..." }],

  "layout_structure": {
    "columns": "1" | "2" | "3" | "4" | "grid" | "unknown",
    "section_count": 0,
    "ordering": ["section1_id", "section2_id"]
  },

  "buttons_and_links": [
    {
      "label": "Start playing",
      "kind": "button" | "link",
      "primary": true | false,
      "x_position": "left" | "center" | "right",
      "row_index": 0
    }
  ],

  "numbers_dates_amounts": [
    { "value": "5", "context": "Start in 5 seconds (kombo / Complexity)" },
    { "value": "K-8", "context": "Full curriculum K-8 (Prodigy / Scope)" }
  ],

  "table_content": {
    "present": true | false,
    "row_count": 4,
    "col_count": 3,
    "header_row": ["", "kombo", "Prodigy"],
    "rows": [["Scope", "Focused on math facts", "Full curriculum K-8"], ...]
  },

  "glyphs_and_icons": [
    { "in_block": "step_card_2", "glyph": "✦", "shape_description": "four-pointed star", "preceding_text": "Earn", "following_text": "Sparks" }
  ],

  "uncertain_items": [
    { "block_id": "...", "concern": "muted grey vs purple eyebrow — possible role distinction" }
  ],

  "below_fold_or_clipped": {
    "appears_clipped": true | false,
    "evidence": "H1 wraps over 5 lines and CTAs typically present in this section are not visible",
    "expected_missing_elements": ["start_playing_cta", "no_signup_required_text"]
  },

  // free-text, OPTIONAL, may be empty
  "interpretation": {
    "semantic_summary": "string",
    "subjective_notes": "string"
  },

  // confidence score, model self-rated
  "confidence": {
    "overall": 0.85,
    "ocr": 0.95,
    "color": 0.6,
    "layout": 0.8
  }
}
```

Key design decisions:
- **closed enum for `image_type`** — model cannot return verbose interpretation in this slot
- **`glyphs_and_icons` as a top-level field** — forces the model to surface non-Latin / icon characters (would have caught the ✦ → + error)
- **`below_fold_or_clipped` as a required field** — directly addresses screenshot 10's failure
- **per-block `color_descriptor`** — prevents the "all eyebrows are purple" bulk hallucination
- **`interpretation` is optional and clearly fenced** — keeps subjective critique out of the observation fields

---

## 9. Recommended preprocessing

Based on observed failures:

| Preprocessing | Recommended? | Reasoning |
|---|---|---|
| Image upscaling | **Yes for mobile screenshots ≤ 400px wide** | The 320×568 stress test (60KB image) is small enough that the model has fewer pixels to read per glyph. 2× nearest-neighbor or Lanczos upscale before forwarding to the VLM should help OCR on narrow-column tables and tight mobile text. |
| Cropping by section | **Yes for table extraction** | Pre-crop the table region and run a dedicated table-extraction pass. The cell-wrap issue on 09 and the 2-col vs 3-col layout disagreement on 03 vs 04 suggest tables benefit from being analyzed in isolation. |
| OCR pre-pass (Tesseract or similar) | **Optional but useful for sanity check** | A tesseract pre-pass that produces a flat text dump can be used as a check on the VLM output: any token in the tesseract output that isn't in the VLM output is a candidate omission. Could specifically flag the ✦ vs + mismatch by detecting unicode in tesseract that becomes ASCII in VLM. |
| Tiling for long screenshots | **Yes for full-page captures, not for viewport** | Not applicable to this dataset since we restricted to viewport screenshots. But the moment the user enables full-page captures, qwen3-vl:8b's input resolution will become a bottleneck. Tile and stitch. |
| Table-specific extraction mode | **Yes — add a separate `extract_table` tool** | This dataset's strongest result was table cell extraction; a dedicated tool with a table-specific prompt and (optionally) a tesseract verification pass could be near-production-ready. |
| Viewport-aware analysis mode | **Yes — add `viewport_hint` parameter** | The MCP server already accepts a custom prompt. Add an optional `viewport_hint` (`desktop` | `tablet` | `mobile` | `small_mobile`) that the server prepends to the system prompt: "this is a `<size>` screenshot — pay specific attention to text wrapping, CTA arrangement, and below-fold content". This would directly target screenshot 10's failure mode. |

---

## 10. Final verdict

### Classification

**pilot-ready** as a private local extraction layer — *not* production-ready.

### Confidence level

Medium-high (≈70%) for OCR on standard marketing/document content. Low (≈30%) for unusual glyphs, icon characters, viewport-edge cases, and color-coded UI signals.

### Why not "production-ready"

The model has stable, repeatable failures (the ✦ glyph error, the FOR TEACHERS color hallucination, missing below-fold detection on small viewports) that would propagate downstream silently. A production layer must either:
- catch these failures via schema validation / pre-processing (the recommendations in §8 and §9), or
- be run side-by-side with a deterministic OCR like tesseract and reconciled.

### Why "pilot-ready" rather than "research-only"

Where the model is good — body text OCR, table cell extraction, button/link enumeration — it is good enough to be useful for a downstream Claude reasoning step. As long as Claude treats the output as a high-recall, medium-precision extraction (and not as ground truth), the pipeline produces value.

### Recommended next test cases

To stress-test what this evaluation could not cover:

1. **Forms with input fields** (text inputs, date pickers, dropdowns, error states) — the kombo page had no forms, so input-field detection is untested.
2. **Numerical-heavy dashboards** (financial pages, metrics dashboards) — to stress the `numbers_dates_amounts` field at scale and check whether the model can read large numbers, decimals, currency symbols, and percentages.
3. **Right-to-left languages** (Arabic, Hebrew) — different text direction is the largest layout-understanding gap a VLM can have.
4. **Charts and graphs** (bar, line, pie) — to check whether the model can read axis labels, legends, and data values.
5. **Screenshots with redactions or partially-loaded skeletons** — to check whether "uncertainty" means anything when content is genuinely incomplete vs. clipped.
6. **Localized text** (non-English UI in the same brand) — to check whether the structural extraction holds up when the language changes.
7. **Dark mode / very low contrast UIs** — color-contrast stress.
8. **Animations frozen as screenshots** (e.g. modal mid-animation, half-loaded state) — to check whether the model identifies transient/loading states.

### Suitability as a private local extraction layer before Claude reasoning

**Yes, with caveats.** For the kombo dataset, qwen3-vl:8b is acceptable as a first-pass extractor that hands off to Claude for reasoning. Key conditions:

- Adopt the structured prompt over the neutral one (table OCR + uncertainty wins outweigh the opinion-leakage issue).
- Add server-level system prompt (§7) and JSON schema validation (§8).
- Add a glyph-aware post-pass to recover the ✦/+ mismatch and similar systematic OCR errors.
- Always include the original screenshot in the handoff to Claude — Claude's vision is materially stronger and can spot things the local model misses (color hallucinations, clipping, alignment errors). The local VLM's role should be **pre-extraction for cost/latency reasons**, not **truth-of-record**.
- For sensitive extraction (tables, numbers), consider ensemble: VLM + tesseract; reconcile differences.

**Bottom line**: shipping today behind the structured prompt and a schema validator is reasonable for an internal pilot. Treating the output as gospel is not.
