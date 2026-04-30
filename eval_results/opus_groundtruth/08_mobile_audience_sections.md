# Opus 4.7 Ground Truth — 08_mobile_audience_sections.png

**viewport:** 390×844 mobile
**section:** FOR KIDS card + FOR PARENTS card (with waitlist link) + FOR TEACHERS card (link clipped below fold)
**analyst:** Claude Opus 4.7 (frontier vision)

```json
{
  "image_type": "webpage_screenshot",
  "viewport_class": "mobile",
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
    {"block_id": "teachers_body", "role": "body", "text": "Classroom tools are on the roadmap. Assign practice, track mastery, and spot who needs help — all from one dashboard.", "x_position": "left", "color_descriptor": "muted-grey", "weight": "regular"}
  ],
  "key_ui_elements": [
    {"kind": "card", "label": "FOR KIDS"},
    {"kind": "card", "label": "FOR PARENTS"},
    {"kind": "card", "label": "FOR TEACHERS", "notes": "eyebrow rendered grey, not purple"},
    {"kind": "link", "label": "Join the parent waitlist →"}
  ],
  "layout_structure": {
    "columns": "1",
    "section_count": 3,
    "ordering": ["FOR KIDS", "FOR PARENTS", "FOR TEACHERS"]
  },
  "buttons_and_links": [
    {"label": "Join the parent waitlist →", "kind": "link", "primary": false, "x_position": "left", "row_index": 1}
  ],
  "numbers_dates_amounts": [],
  "table_content": {"present": false, "row_count": 0, "col_count": 0, "header_row": [], "rows": []},
  "glyphs_and_icons": [
    {"in_block": "kids_heading", "glyph": "—", "shape_description": "em dash"},
    {"in_block": "parents_body", "glyph": "—", "shape_description": "em dash"},
    {"in_block": "teachers_body", "glyph": "—", "shape_description": "em dash"},
    {"in_block": "parents_link", "glyph": "→", "shape_description": "right arrow"}
  ],
  "uncertain_items": [],
  "below_fold_or_clipped": {
    "appears_clipped": true,
    "evidence": "FOR TEACHERS body is visible but the 'Join the teacher waitlist →' link below it is not in frame",
    "expected_missing_elements": ["Join the teacher waitlist link", "HOW IT WORKS step grid", "WHY KOMBO comparison table"]
  },
  "interpretation": {
    "semantic_summary": "Mobile vertical stack of three audience-segment cards",
    "subjective_notes": ""
  },
  "confidence": {"overall": 0.99, "ocr": 1.0, "color": 0.94, "layout": 0.99}
}
```

## Notes (frontier observations)
- The teacher waitlist link is below the fold — only the parent waitlist link is visible.
- FOR TEACHERS eyebrow is grey, consistent with desktop/tablet.
