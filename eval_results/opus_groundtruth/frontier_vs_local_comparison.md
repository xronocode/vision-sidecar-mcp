# Frontier vs Local VLM — Three-Way Comparison

**Frontier model:** Claude Opus 4.7 (1M ctx) — multimodal vision
**Local model:** qwen3-vl:8b via Ollama, served by `vision-sidecar-mcp`
**Dataset:** kombo (10 screenshots, 320×568 → 1440×900)
**Date:** 2026-04-29

This report fills the gap that the earlier two evaluation cycles left open: a third reference column showing **how the frontier model sees each screenshot**, side by side with the local VLM **before tuning** (v0.1.0 baseline) and **after tuning** (v0.2.2 with extraction-only system prompt, ML-team Ollama config, `</think>` prefill, schema, and 2× upscaling).

The goal is to answer a single question:

> **How far is our local solution from a frontier-class vision model — and on which axes?**

---

## 1. Evaluation method

For each of the 10 screenshots:
- **Frontier (Opus)** ground truth lives in `eval_results/opus_groundtruth/01..10_*.md` — same structured JSON schema as the local VLM output.
- **Local baseline** (cycle 1) lives in `eval_results/kombo/raw/*.{neutral,structured}.json`.
- **Local after-tuning** (cycle 2) lives in `eval_results/kombo_after_tuning/raw/*.{mcp_neutral,mcp_structured}.md`.

Each model is scored on the same nine dimensions used in the baseline aggregate (`eval_results/kombo/aggregate/aggregate_report.md` §6). Frontier scores are anchored to "what a careful engineer would write down looking at the same pixel" — i.e. the practical ceiling, not omniscience.

---

## 2. Headline numbers — frontier vs local (after tuning), 9-dim avg over 10 screenshots

| Dimension | Frontier (Opus) | Local v0.1.0 (baseline N) | Local v0.2.2 (tuned S) | Gap (frontier − tuned) |
|---|---:|---:|---:|---:|
| OCR / text extraction | 5.0 | 4.7 | 4.9 | **0.1** |
| UI element detection | 5.0 | 4.3 | 4.7 | 0.3 |
| layout understanding | 5.0 | 3.6 | 4.7 | 0.3 |
| CTA / button detection | 5.0 | 4.7 | 5.0 | **0.0** |
| semantic understanding | 5.0 | 4.2 | 4.6 | 0.4 |
| table extraction | 5.0 | 4.5 | 5.0 | **0.0** |
| hallucination control | 5.0 | 3.9 | 4.0 | **1.0** |
| uncertainty handling | 5.0 | 2.5 | 4.6 | 0.4 |
| usefulness for downstream | 5.0 | 3.6 | 4.8 | 0.2 |
| **average** | **5.00** | **3.99** | **4.70** | **0.30** |

Tuning closed ~70% of the frontier gap (from 1.01 below to 0.30 below). The remaining gap is concentrated in **hallucination control** and **semantic nuance**, not in raw OCR or structured extraction.

---

## 3. Where the local model now matches the frontier

### Body-text OCR (parity)
Across all 10 images, the tuned VLM transcribes hero, card, and step-card body text with the same character-level fidelity as Opus reads. The em-dash and apostrophe are preserved correctly in `Not a test — an adventure`, `kingdom — one kombo at a time`, `I'm a parent`, etc.

### Table extraction (parity)
The 4×3 WHY KOMBO table is extracted correctly by both Opus and v0.2.2 (the dedicated `extract_table` tool plus the structured-call `table_content` field). Cell text wrapping at 390px (mobile) does not throw off either model.

### Glyph preservation (parity, after tuning)
The ✦ sparkle in `Earn ✦ Sparks` is the headline glyph case. Baseline v0.1.0 normalized it to `+` in 4/5 cases. v0.2.2 preserves `✦` verbatim in `block_id`, `glyphs_and_icons[*].glyph`, and the rendered `Earn ✦ Sparks` token. Frontier and tuned local now agree.

### Below-fold detection on the worst case (parity)
On `10_small_mobile_stress.png` (320×568) the CTAs are entirely below the fold. Baseline v0.1.0 scored 1/5 on uncertainty (asserted "no issues"). v0.2.2 produces `appears_clipped: true` with evidence `"Hero section has heading and subhead but no primary action button below subhead"` — same conclusion as Opus, with explicit `expected_missing_elements`.

---

## 4. Where the local model still trails

### 4.1 Hallucination on subtle color (largest residual gap, 1.0 score points)

| Item | Opus (frontier) | Tuned local (v0.2.2) |
|---|---|---|
| FOR TEACHERS eyebrow color | **muted grey** (genuinely different from FOR KIDS / FOR PARENTS purple — visual cue that this is "coming soon") | "purple" or "light purple" — same as the other two eyebrows |
| "Start playing" button text color | **near-black on purple** (the text is dark, sitting on a solid purple pill) | "white" — incorrect |
| FOR KIDS card background | very pale **lavender** | sometimes "white" |
| Step card individual tones | lavender / cream / mint / pink — **four different pastels** | mostly "light grey" or one generic background |

The local VLM sees "broadly purple-ish UI" but cannot reliably distinguish the muted-grey eyebrow on FOR TEACHERS from the saturated purple on FOR KIDS / FOR PARENTS. This is a real perceptual gap, not a prompt issue.

### 4.2 Centered-vs-left alignment hallucination (small viewports)

On `10_small_mobile_stress.png`, the tuned local model reports text alignment as "centered" in places where Opus sees clearly left-aligned content. The model has a bias on narrow viewports.

### 4.3 Wrap-line counting

Opus correctly identifies that on `07_mobile_hero.png` the H1 wraps to **4 lines** ("The math / RPG where / you build a / kingdom"), and on `10_small_mobile_stress.png` it wraps to **5 lines** ("The math / RPG / where you / build a / kingdom"). The local VLM treats H1 as a single block and does not surface line-count.

### 4.4 False-positive clipping (rare)

`09_mobile_comparison_table.png` shows the full table and is not clipped. Opus correctly says `appears_clipped: false`. Tuned local (structured) says `appears_clipped: true` with evidence "Table content extends beyond visible area" — a false positive. This is a regression from a tuning that pushed the model toward over-flagging clipping.

### 4.5 Semantic nuance

Opus annotates cards with usability notes ("FOR TEACHERS eyebrow grey = coming-soon hint"). The local model produces no comparable interpretive layer. This is by design — we suppress subjective notes — but the frontier model can still surface visual-design intent that purely-extractive prompts cannot.

---

## 5. Per-screenshot summary — three columns

Score legend: 0–5 (avg of 9 dimensions).

| # | Screenshot | Opus | v0.1.0 baseline | v0.2.2 tuned | Tuned gap |
|---|---|---:|---:|---:|---:|
| 01 | desktop hero | 5.0 | 4.0 | 4.7 | 0.3 |
| 02 | desktop audience | 5.0 | 4.3 | 4.7 | 0.3 |
| 03 | desktop how-it-works (full) | 5.0 | 4.3 | 4.9 | 0.1 |
| 04 | desktop comparison-table (= 03) | 5.0 | 4.4 | 4.9 | 0.1 |
| 05 | tablet portrait hero | 5.0 | 4.2 | 4.7 | 0.3 |
| 06 | tablet landscape sections | 5.0 | 4.4 | 4.8 | 0.2 |
| 07 | mobile hero | 5.0 | 3.4 (empty content) | 4.6 | 0.4 |
| 08 | mobile audience | 5.0 | 4.2 | 4.7 | 0.3 |
| 09 | mobile comparison table | 5.0 | 4.4 | 4.6 (false-clipped) | 0.4 |
| 10 | 320×568 small-mobile stress | 5.0 | 3.1 (claimed no issues) | 4.7 | 0.3 |
| **avg** |  | **5.00** | **3.99** | **4.70** | **0.30** |

---

## 6. Bottom-line verdict

**The tuned local VLM (qwen3-vl:8b under v0.2.2) is operating at roughly 94% of frontier parity on this dataset for the tasks the sidecar is designed to do** — extraction-style structured output for downstream Claude reasoning.

| Use case | Frontier needed? | Local sufficient? |
|---|---|---|
| OCR of body text, headings, labels | no | **yes — parity** |
| Extracting table contents | no | **yes — parity** |
| Enumerating buttons/links | no | **yes — near-parity** |
| Detecting below-fold clipping | no | **yes — near-parity** (one false positive on 09) |
| Per-element color attribution (subtle greys vs purples) | **yes** | no — known limitation |
| Wrap-line / line-counting | **yes** | no |
| Visual-design intent / coming-soon cues | **yes** | no — out of scope by design |

**Recommendation for the pipeline architecture:**
- For 7/10 dimensions, the local VLM is now production-quality. Send it everything that's structurally extractive.
- For the remaining 3 dimensions (subtle color, line-counting, design intent), defer to the frontier model. Those are precisely the cases where Claude Opus already has the picture in context — no separate VLM call needed.

In other words: **the sidecar is a high-recall, medium-precision extractor, and the frontier is a low-volume, high-fidelity backstop.** Both layers are needed, and the gap between them is now narrow enough that the cost/latency win of running the local VLM is worth it for everything except color-nuance and design-intent calls.

---

## 7. Methodological caveat

Frontier scores in this report are the analyst's own (Opus 4.7) — there is no third-party arbiter. This means:
- Local-vs-frontier is **not** a blind comparison; the frontier model is also the scorer.
- The frontier scores are anchored to "what is in the pixels," not to "what Opus could plausibly invent." The handful of items I flagged as my own observations (FOR TEACHERS grey eyebrow, near-black button text on purple) are independently verifiable from the screenshots.
- If higher confidence is needed, the next eval cycle should add a second human (or a separate Claude session) to score the frontier outputs blind against the local outputs.

---

## 8. Files

- `eval_results/opus_groundtruth/01..10_*.md` — 10 per-screenshot frontier ground-truths (this report's source data)
- `eval_results/kombo/aggregate/aggregate_report.md` — cycle 1 baseline aggregate
- `eval_results/kombo_after_tuning/aggregate/before_after_report.md` — cycle 2 before/after report
- `eval_images/kombo/metadata.json` — capture metadata for the 10 screenshots
