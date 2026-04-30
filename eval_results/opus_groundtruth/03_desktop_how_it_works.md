# Opus 4.7 Ground Truth — 03_desktop_how_it_works.png

**viewport:** 1440×900 desktop
**section:** Tail of FOR PARENTS link + full FOR TEACHERS card + HOW IT WORKS step grid + WHY KOMBO comparison table
**analyst:** Claude Opus 4.7 (frontier vision)
**note:** byte-identical to 04_desktop_comparison_table.png (page bottoms out at scrollY=973)

```json
{
  "image_type": "webpage_screenshot",
  "viewport_class": "desktop",
  "visible_text": [
    {"block_id": "parents_link", "role": "link", "text": "Join the parent waitlist →", "x_position": "left", "color_descriptor": "purple", "weight": "bold"},
    {"block_id": "teachers_eyebrow", "role": "eyebrow", "text": "FOR TEACHERS", "x_position": "left", "color_descriptor": "muted-grey", "weight": "regular"},
    {"block_id": "teachers_heading", "role": "heading_h2", "text": "Zero prep, full visibility", "x_position": "left", "color_descriptor": "near-black", "weight": "bold"},
    {"block_id": "teachers_body", "role": "body", "text": "Classroom tools are on the roadmap. Assign practice, track mastery, and spot who needs help — all from one dashboard.", "x_position": "left", "color_descriptor": "muted-grey", "weight": "regular"},
    {"block_id": "teachers_link", "role": "link", "text": "Join the teacher waitlist →", "x_position": "left", "color_descriptor": "purple", "weight": "bold"},
    {"block_id": "how_eyebrow", "role": "eyebrow", "text": "HOW IT WORKS", "x_position": "left", "color_descriptor": "purple", "weight": "regular"},
    {"block_id": "step1_h", "role": "heading_h3", "text": "Practice math", "x_position": "left", "color_descriptor": "near-black", "weight": "bold"},
    {"block_id": "step1_b", "role": "body", "text": "Solve problems at your level", "x_position": "left", "color_descriptor": "muted-grey", "weight": "regular"},
    {"block_id": "step2_h", "role": "heading_h3", "text": "Earn ✦ Sparks", "x_position": "left", "color_descriptor": "near-black", "weight": "bold"},
    {"block_id": "step2_b", "role": "body", "text": "Every correct answer counts", "x_position": "left", "color_descriptor": "muted-grey", "weight": "regular"},
    {"block_id": "step3_h", "role": "heading_h3", "text": "Build kingdom", "x_position": "left", "color_descriptor": "near-black", "weight": "bold"},
    {"block_id": "step3_b", "role": "body", "text": "Grow your world with sparks", "x_position": "left", "color_descriptor": "muted-grey", "weight": "regular"},
    {"block_id": "step4_h", "role": "heading_h3", "text": "Want more", "x_position": "left", "color_descriptor": "near-black", "weight": "bold"},
    {"block_id": "step4_b", "role": "body", "text": "Unlock regions and earn rewards", "x_position": "left", "color_descriptor": "muted-grey", "weight": "regular"},
    {"block_id": "why_eyebrow", "role": "eyebrow", "text": "WHY KOMBO", "x_position": "left", "color_descriptor": "purple", "weight": "regular"}
  ],
  "key_ui_elements": [
    {"kind": "card", "label": "FOR TEACHERS", "notes": "muted lavender-grey card"},
    {"kind": "link", "label": "Join the teacher waitlist →", "notes": "purple text with right arrow"},
    {"kind": "card", "label": "Practice math", "notes": "lavender pastel"},
    {"kind": "card", "label": "Earn ✦ Sparks", "notes": "cream/yellow pastel"},
    {"kind": "card", "label": "Build kingdom", "notes": "mint/teal pastel"},
    {"kind": "card", "label": "Want more", "notes": "pink pastel"},
    {"kind": "table", "label": "WHY KOMBO comparison", "notes": "two-product comparison table, four attribute rows"}
  ],
  "layout_structure": {
    "columns": "1 stacked + 4-col step grid + 3-col table",
    "section_count": 3,
    "ordering": ["FOR TEACHERS card", "HOW IT WORKS step grid", "WHY KOMBO comparison table"]
  },
  "buttons_and_links": [
    {"label": "Join the parent waitlist →", "kind": "link", "primary": false, "x_position": "left", "row_index": 0},
    {"label": "Join the teacher waitlist →", "kind": "link", "primary": false, "x_position": "left", "row_index": 1}
  ],
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
    {"in_block": "teachers_body", "glyph": "—", "shape_description": "em dash", "preceding_text": "spot who needs help", "following_text": "all from one dashboard"},
    {"in_block": "parents_link", "glyph": "→", "shape_description": "right arrow"},
    {"in_block": "teachers_link", "glyph": "→", "shape_description": "right arrow"},
    {"in_block": "step2_h", "glyph": "✦", "shape_description": "four-pointed sparkle", "preceding_text": "Earn", "following_text": "Sparks"}
  ],
  "uncertain_items": [],
  "below_fold_or_clipped": {
    "appears_clipped": false,
    "evidence": "Comparison table appears complete (4 rows, 3 columns); no truncated text",
    "expected_missing_elements": []
  },
  "interpretation": {
    "semantic_summary": "Process explanation (4 steps) followed by competitive comparison vs Prodigy",
    "subjective_notes": ""
  },
  "confidence": {"overall": 0.99, "ocr": 1.0, "color": 0.93, "layout": 0.99}
}
```

## Notes (frontier observations)
- FOR TEACHERS eyebrow color is genuinely different from the other two (grey, not purple) — visual hierarchy hint that this is a "coming soon" card.
- The header column under "kombo" has lowercase 'k' (matches logo); local VLM sometimes capitalizes.
- Table is 4 data rows × 3 columns (row label + 2 product columns).
