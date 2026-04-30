# Opus 4.7 Ground Truth — 07_mobile_hero.png

**viewport:** 390×844 mobile (iPhone 14 Pro size)
**section:** Top nav + hero card with wrapped H1 + start of FOR KIDS
**analyst:** Claude Opus 4.7 (frontier vision)

```json
{
  "image_type": "webpage_screenshot",
  "viewport_class": "mobile",
  "visible_text": [
    {"block_id": "nav_logo", "role": "nav", "text": "kombo", "x_position": "left", "color_descriptor": "near-black", "weight": "bold"},
    {"block_id": "nav_play", "role": "nav", "text": "Play", "x_position": "right", "color_descriptor": "near-black", "weight": "regular"},
    {"block_id": "nav_progress", "role": "nav", "text": "Progress", "x_position": "right", "color_descriptor": "near-black", "weight": "regular"},
    {"block_id": "eyebrow", "role": "eyebrow", "text": "READY TO PLAY", "x_position": "left", "color_descriptor": "purple", "weight": "regular"},
    {"block_id": "h1_l1", "role": "heading_h1", "text": "The math", "x_position": "left", "color_descriptor": "near-black", "weight": "bold"},
    {"block_id": "h1_l2", "role": "heading_h1", "text": "RPG where", "x_position": "left", "color_descriptor": "near-black", "weight": "bold"},
    {"block_id": "h1_l3", "role": "heading_h1", "text": "you build a", "x_position": "left", "color_descriptor": "near-black", "weight": "bold"},
    {"block_id": "h1_l4", "role": "heading_h1", "text": "kingdom", "x_position": "left", "color_descriptor": "near-black", "weight": "bold"},
    {"block_id": "subhead", "role": "body", "text": "Practice multiplication and division, earn sparks, and grow your kingdom — one kombo at a time.", "x_position": "left", "color_descriptor": "muted-grey", "weight": "regular"},
    {"block_id": "cta_primary", "role": "button_label", "text": "Start playing", "x_position": "left", "color_descriptor": "near-black", "weight": "regular"},
    {"block_id": "cta_parent", "role": "button_label", "text": "I'm a parent", "x_position": "left", "color_descriptor": "near-black", "weight": "regular"},
    {"block_id": "cta_teacher", "role": "button_label", "text": "I'm a teacher", "x_position": "left", "color_descriptor": "near-black", "weight": "regular"},
    {"block_id": "no_signup", "role": "body", "text": "No sign-up required", "x_position": "left", "color_descriptor": "muted-grey", "weight": "regular"},
    {"block_id": "kids_eyebrow", "role": "eyebrow", "text": "FOR KIDS", "x_position": "left", "color_descriptor": "purple", "weight": "regular"},
    {"block_id": "kids_heading", "role": "heading_h2", "text": "Not a test — an adventure", "x_position": "left", "color_descriptor": "near-black", "weight": "bold"}
  ],
  "key_ui_elements": [
    {"kind": "button", "label": "Start playing", "notes": "primary CTA, solid purple pill"},
    {"kind": "button", "label": "I'm a parent", "notes": "secondary, white pill"},
    {"kind": "button", "label": "I'm a teacher", "notes": "secondary, white pill, on second row"},
    {"kind": "button", "label": "Play", "notes": "nav pill"},
    {"kind": "button", "label": "Progress", "notes": "nav pill"}
  ],
  "layout_structure": {
    "columns": "1",
    "section_count": 2,
    "ordering": ["top nav", "hero card with wrapped H1 (4 lines)", "FOR KIDS heading"]
  },
  "buttons_and_links": [
    {"label": "Play", "kind": "button", "primary": false, "x_position": "right", "row_index": 0},
    {"label": "Progress", "kind": "button", "primary": false, "x_position": "right", "row_index": 0},
    {"label": "Start playing", "kind": "button", "primary": true, "x_position": "left", "row_index": 1},
    {"label": "I'm a parent", "kind": "button", "primary": false, "x_position": "right", "row_index": 1},
    {"label": "I'm a teacher", "kind": "button", "primary": false, "x_position": "left", "row_index": 2}
  ],
  "numbers_dates_amounts": [],
  "table_content": {"present": false, "row_count": 0, "col_count": 0, "header_row": [], "rows": []},
  "glyphs_and_icons": [
    {"in_block": "subhead", "glyph": "—", "shape_description": "em dash"},
    {"in_block": "kids_heading", "glyph": "—", "shape_description": "em dash"}
  ],
  "uncertain_items": [],
  "below_fold_or_clipped": {
    "appears_clipped": true,
    "evidence": "FOR KIDS body text and rest of page below fold; only kids heading visible",
    "expected_missing_elements": ["FOR KIDS body", "FOR PARENTS section", "FOR TEACHERS section", "HOW IT WORKS", "WHY KOMBO comparison table"]
  },
  "interpretation": {
    "semantic_summary": "Mobile rendering of hero — H1 wraps over 4 lines, CTAs wrap to 2 rows",
    "subjective_notes": ""
  },
  "confidence": {"overall": 0.99, "ocr": 1.0, "color": 0.94, "layout": 0.99}
}
```

## Notes (frontier observations)
- H1 wraps to 4 lines: "The math" / "RPG where" / "you build a" / "kingdom".
- CTAs wrap to 2 rows: "Start playing" + "I'm a parent" on row 1; "I'm a teacher" on row 2.
- Egg illustration is gone (responsive rule).
- This is the screenshot where the local VLM with viewport_hint=mobile deterministically returned empty content in cycle 1 baseline — fixed in v0.2.2.
