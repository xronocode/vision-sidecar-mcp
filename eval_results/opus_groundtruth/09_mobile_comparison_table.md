# Opus 4.7 Ground Truth — 09_mobile_comparison_table.png

**viewport:** 390×844 mobile
**section:** Tail of HOW IT WORKS step cards + full WHY KOMBO comparison table
**analyst:** Claude Opus 4.7 (frontier vision)

```json
{
  "image_type": "webpage_screenshot",
  "viewport_class": "mobile",
  "visible_text": [
    {"block_id": "step1_h", "role": "heading_h3", "text": "Practice math", "x_position": "center", "color_descriptor": "near-black", "weight": "bold"},
    {"block_id": "step1_b", "role": "body", "text": "Solve problems at your level", "x_position": "center", "color_descriptor": "muted-grey", "weight": "regular"},
    {"block_id": "step2_h", "role": "heading_h3", "text": "Earn ✦ Sparks", "x_position": "center", "color_descriptor": "near-black", "weight": "bold"},
    {"block_id": "step2_b", "role": "body", "text": "Every correct answer counts", "x_position": "center", "color_descriptor": "muted-grey", "weight": "regular"},
    {"block_id": "step3_h", "role": "heading_h3", "text": "Build kingdom", "x_position": "center", "color_descriptor": "near-black", "weight": "bold"},
    {"block_id": "step3_b", "role": "body", "text": "Grow your world with sparks", "x_position": "center", "color_descriptor": "muted-grey", "weight": "regular"},
    {"block_id": "step4_h", "role": "heading_h3", "text": "Want more", "x_position": "center", "color_descriptor": "near-black", "weight": "bold"},
    {"block_id": "step4_b", "role": "body", "text": "Unlock regions and earn rewards", "x_position": "center", "color_descriptor": "muted-grey", "weight": "regular"},
    {"block_id": "why_eyebrow", "role": "eyebrow", "text": "WHY KOMBO", "x_position": "left", "color_descriptor": "purple", "weight": "regular"}
  ],
  "key_ui_elements": [
    {"kind": "card", "label": "Practice math", "notes": "lavender step card, centered text"},
    {"kind": "card", "label": "Earn ✦ Sparks", "notes": "cream/yellow step card with sparkle glyph"},
    {"kind": "card", "label": "Build kingdom", "notes": "mint step card"},
    {"kind": "card", "label": "Want more", "notes": "pink step card"},
    {"kind": "table", "label": "WHY KOMBO comparison", "notes": "4 rows × 3 cols (label + kombo + Prodigy), cells wrap multi-line"}
  ],
  "layout_structure": {
    "columns": "1 stack of step cards + 3-col table",
    "section_count": 2,
    "ordering": ["HOW IT WORKS step cards", "WHY KOMBO comparison table"]
  },
  "buttons_and_links": [],
  "numbers_dates_amounts": [
    {"value": "5", "context": "Start in 5 seconds (Complexity row, kombo column)"}
  ],
  "table_content": {
    "present": true,
    "row_count": 4,
    "col_count": 3,
    "header_row": ["", "kombo", "Prodigy"],
    "rows": [
      ["Scope", "Focused on math facts", "Full curriculum K-8"],
      ["Core skill", "Speed and retention", "Conceptual understanding"],
      ["Complexity", "Start in 5 seconds", "Setup and onboarding"],
      ["Philosophy", "Free, no ads, no paywalls", "Freemium with membership"]
    ]
  },
  "glyphs_and_icons": [
    {"in_block": "step2_h", "glyph": "✦", "shape_description": "four-pointed sparkle", "preceding_text": "Earn", "following_text": "Sparks"}
  ],
  "uncertain_items": [],
  "below_fold_or_clipped": {
    "appears_clipped": false,
    "evidence": "Full table visible with all 4 rows; bottom of page reached",
    "expected_missing_elements": []
  },
  "interpretation": {
    "semantic_summary": "Mobile rendering of process steps + competitive comparison table",
    "subjective_notes": ""
  },
  "confidence": {"overall": 0.99, "ocr": 1.0, "color": 0.94, "layout": 0.99}
}
```

## Notes (frontier observations)
- Step cards are full-width and stacked vertically on mobile (vs 4-col grid on desktop).
- Each step card has a distinct pastel background color, like desktop.
- Table cells wrap over 2 lines because the 3-column layout is squeezed at 390px.
