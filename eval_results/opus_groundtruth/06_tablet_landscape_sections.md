# Opus 4.7 Ground Truth — 06_tablet_landscape_sections.png

**viewport:** 1024×768 tablet landscape
**section:** Three audience cards (FOR KIDS, FOR PARENTS, FOR TEACHERS) + tiny strip of next section
**analyst:** Claude Opus 4.7 (frontier vision)

```json
{
  "image_type": "webpage_screenshot",
  "viewport_class": "tablet",
  "visible_text": [
    {"block_id": "kids_eyebrow", "role": "eyebrow", "text": "FOR KIDS", "x_position": "left", "color_descriptor": "purple", "weight": "regular"},
    {"block_id": "kids_heading", "role": "heading_h2", "text": "Not a test — an adventure", "x_position": "left", "color_descriptor": "near-black", "weight": "bold"},
    {"block_id": "kids_body", "role": "body", "text": "Solve math problems to earn sparks. Use sparks to build your kingdom. Each correct answer makes your world bigger.", "x_position": "left", "color_descriptor": "muted-grey", "weight": "regular"},
    {"block_id": "parents_eyebrow", "role": "eyebrow", "text": "FOR PARENTS", "x_position": "left", "color_descriptor": "purple", "weight": "regular"},
    {"block_id": "parents_heading", "role": "heading_h2", "text": "Math practice without the nagging", "x_position": "left", "color_descriptor": "near-black", "weight": "bold"},
    {"block_id": "parents_body", "role": "body", "text": "A parent dashboard is on the way. See progress, set goals, and stay informed — without turning into homework police.", "x_position": "left", "color_descriptor": "muted-grey", "weight": "regular"},
    {"block_id": "parents_link", "role": "link", "text": "Join the parent waitlist →", "x_position": "left", "color_descriptor": "purple", "weight": "bold"},
    {"block_id": "teachers_eyebrow", "role": "eyebrow", "text": "FOR TEACHERS", "x_position": "left", "color_descriptor": "muted-grey", "weight": "regular"},
    {"block_id": "teachers_heading", "role": "heading_h2", "text": "Zero prep, full visibility", "x_position": "left", "color_descriptor": "near-black", "weight": "bold"},
    {"block_id": "teachers_body", "role": "body", "text": "Classroom tools are on the roadmap. Assign practice, track mastery, and spot who needs help — all from one dashboard.", "x_position": "left", "color_descriptor": "muted-grey", "weight": "regular"},
    {"block_id": "teachers_link", "role": "link", "text": "Join the teacher waitlist →", "x_position": "left", "color_descriptor": "purple", "weight": "bold"}
  ],
  "key_ui_elements": [
    {"kind": "card", "label": "FOR KIDS", "notes": "lavender background"},
    {"kind": "card", "label": "FOR PARENTS", "notes": "lavender background"},
    {"kind": "card", "label": "FOR TEACHERS", "notes": "lavender-grey background, eyebrow rendered grey not purple"},
    {"kind": "link", "label": "Join the parent waitlist →"},
    {"kind": "link", "label": "Join the teacher waitlist →"}
  ],
  "layout_structure": {
    "columns": "1",
    "section_count": 3,
    "ordering": ["FOR KIDS", "FOR PARENTS", "FOR TEACHERS"]
  },
  "buttons_and_links": [
    {"label": "Join the parent waitlist →", "kind": "link", "primary": false, "x_position": "left", "row_index": 1},
    {"label": "Join the teacher waitlist →", "kind": "link", "primary": false, "x_position": "left", "row_index": 2}
  ],
  "numbers_dates_amounts": [],
  "table_content": {"present": false, "row_count": 0, "col_count": 0, "header_row": [], "rows": []},
  "glyphs_and_icons": [
    {"in_block": "kids_heading", "glyph": "—", "shape_description": "em dash"},
    {"in_block": "parents_body", "glyph": "—", "shape_description": "em dash"},
    {"in_block": "teachers_body", "glyph": "—", "shape_description": "em dash"},
    {"in_block": "parents_link", "glyph": "→", "shape_description": "right arrow"},
    {"in_block": "teachers_link", "glyph": "→", "shape_description": "right arrow"}
  ],
  "uncertain_items": [],
  "below_fold_or_clipped": {
    "appears_clipped": true,
    "evidence": "Thin strip of next section visible at bottom; HOW IT WORKS step grid not visible",
    "expected_missing_elements": ["HOW IT WORKS step grid", "WHY KOMBO comparison table"]
  },
  "interpretation": {
    "semantic_summary": "Three audience-segment cards stacked vertically",
    "subjective_notes": ""
  },
  "confidence": {"overall": 0.99, "ocr": 1.0, "color": 0.94, "layout": 0.99}
}
```

## Notes (frontier observations)
- FOR TEACHERS eyebrow is genuinely grey, not purple — same as in 02/03.
- All three cards show waitlist links here (parent + teacher).
