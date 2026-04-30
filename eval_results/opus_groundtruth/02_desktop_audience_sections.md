# Opus 4.7 Ground Truth — 02_desktop_audience_sections.png

**viewport:** 1440×900 desktop
**section:** Three audience cards (FOR KIDS, FOR PARENTS, FOR TEACHERS) + start of HOW IT WORKS
**analyst:** Claude Opus 4.7 (frontier vision)

```json
{
  "image_type": "webpage_screenshot",
  "viewport_class": "desktop",
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
    {"block_id": "teachers_link", "role": "link", "text": "Join the teacher waitlist →", "x_position": "left", "color_descriptor": "purple", "weight": "bold"},
    {"block_id": "how_eyebrow", "role": "eyebrow", "text": "HOW IT WORKS", "x_position": "left", "color_descriptor": "purple", "weight": "regular"},
    {"block_id": "step1_heading", "role": "heading_h3", "text": "Practice math", "x_position": "left", "color_descriptor": "near-black", "weight": "bold"},
    {"block_id": "step1_body", "role": "body", "text": "Solve problems at your level", "x_position": "left", "color_descriptor": "muted-grey", "weight": "regular"},
    {"block_id": "step2_heading", "role": "heading_h3", "text": "Earn ✦ Sparks", "x_position": "left", "color_descriptor": "near-black", "weight": "bold"},
    {"block_id": "step2_body", "role": "body", "text": "Every correct answer counts", "x_position": "left", "color_descriptor": "muted-grey", "weight": "regular"},
    {"block_id": "step3_heading", "role": "heading_h3", "text": "Build kingdom", "x_position": "left", "color_descriptor": "near-black", "weight": "bold"},
    {"block_id": "step3_body", "role": "body", "text": "Grow your world with sparks", "x_position": "left", "color_descriptor": "muted-grey", "weight": "regular"},
    {"block_id": "step4_heading", "role": "heading_h3", "text": "Want more", "x_position": "left", "color_descriptor": "near-black", "weight": "bold"},
    {"block_id": "step4_body", "role": "body", "text": "Unlock regions and earn rewards", "x_position": "left", "color_descriptor": "muted-grey", "weight": "regular"}
  ],
  "key_ui_elements": [
    {"kind": "card", "label": "FOR KIDS", "notes": "lavender background"},
    {"kind": "card", "label": "FOR PARENTS", "notes": "lighter lavender background"},
    {"kind": "card", "label": "FOR TEACHERS", "notes": "muted lavender-grey background — slightly different tone, eyebrow rendered in grey not purple"},
    {"kind": "card", "label": "Practice math", "notes": "lavender step card"},
    {"kind": "card", "label": "Earn ✦ Sparks", "notes": "warm cream/yellow step card with star glyph"},
    {"kind": "card", "label": "Build kingdom", "notes": "pale teal/mint step card"},
    {"kind": "card", "label": "Want more", "notes": "pale pink step card"},
    {"kind": "link", "label": "Join the parent waitlist →", "notes": "purple text with right arrow"},
    {"kind": "link", "label": "Join the teacher waitlist →", "notes": "purple text with right arrow"}
  ],
  "layout_structure": {
    "columns": "1 (audience cards stacked) + 4-column step grid below",
    "section_count": 4,
    "ordering": ["FOR KIDS card", "FOR PARENTS card", "FOR TEACHERS card", "HOW IT WORKS step grid"]
  },
  "buttons_and_links": [
    {"label": "Join the parent waitlist →", "kind": "link", "primary": false, "x_position": "left", "row_index": 1},
    {"label": "Join the teacher waitlist →", "kind": "link", "primary": false, "x_position": "left", "row_index": 2}
  ],
  "numbers_dates_amounts": [],
  "table_content": {"present": false, "row_count": 0, "col_count": 0, "header_row": [], "rows": []},
  "glyphs_and_icons": [
    {"in_block": "kids_heading", "glyph": "—", "shape_description": "em dash", "preceding_text": "Not a test", "following_text": "an adventure"},
    {"in_block": "parents_body", "glyph": "—", "shape_description": "em dash", "preceding_text": "stay informed", "following_text": "without turning"},
    {"in_block": "teachers_body", "glyph": "—", "shape_description": "em dash", "preceding_text": "spot who needs help", "following_text": "all from one dashboard"},
    {"in_block": "parents_link", "glyph": "→", "shape_description": "right arrow", "preceding_text": "waitlist", "following_text": ""},
    {"in_block": "teachers_link", "glyph": "→", "shape_description": "right arrow", "preceding_text": "waitlist", "following_text": ""},
    {"in_block": "step2_heading", "glyph": "✦", "shape_description": "four-pointed star (sparkle glyph)", "preceding_text": "Earn", "following_text": "Sparks"}
  ],
  "uncertain_items": [],
  "below_fold_or_clipped": {
    "appears_clipped": true,
    "evidence": "Step cards are visible but the WHY KOMBO comparison table beneath them is not",
    "expected_missing_elements": ["WHY KOMBO comparison table"]
  },
  "interpretation": {
    "semantic_summary": "Three audience-segmented value props (kids/parents/teachers) plus a four-step visual flow describing the product loop",
    "subjective_notes": ""
  },
  "confidence": {"overall": 0.98, "ocr": 1.0, "color": 0.92, "layout": 0.99}
}
```

## Notes (frontier observations)
- FOR TEACHERS eyebrow is rendered in muted grey, **not** the same purple as the other two eyebrows — this is a real visual difference, not a hallucination. The local VLM consistently sees it as the same purple.
- Step 2 card uses a warm cream/yellow tone; the ✦ glyph between "Earn" and "Sparks" is a four-pointed sparkle (often misread as `+`).
- Step cards have distinct pastel colors per card (lavender/cream/mint/pink) — accent variety, not all the same.
