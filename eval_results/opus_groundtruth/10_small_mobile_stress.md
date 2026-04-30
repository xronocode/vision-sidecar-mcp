# Opus 4.7 Ground Truth — 10_small_mobile_stress.png

**viewport:** 320×568 small mobile (legacy iPhone SE)
**section:** Top nav + hero card with H1 over 5 lines + clipped subhead at bottom edge
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
    {"block_id": "h1_l2", "role": "heading_h1", "text": "RPG", "x_position": "left", "color_descriptor": "near-black", "weight": "bold"},
    {"block_id": "h1_l3", "role": "heading_h1", "text": "where you", "x_position": "left", "color_descriptor": "near-black", "weight": "bold"},
    {"block_id": "h1_l4", "role": "heading_h1", "text": "build a", "x_position": "left", "color_descriptor": "near-black", "weight": "bold"},
    {"block_id": "h1_l5", "role": "heading_h1", "text": "kingdom", "x_position": "left", "color_descriptor": "near-black", "weight": "bold"},
    {"block_id": "subhead", "role": "body", "text": "Practice multiplication and division, earn sparks, and grow your kingdom — one kombo at a time.", "x_position": "left", "color_descriptor": "muted-grey", "weight": "regular"}
  ],
  "key_ui_elements": [
    {"kind": "button", "label": "Play", "notes": "nav pill"},
    {"kind": "button", "label": "Progress", "notes": "nav pill"}
  ],
  "layout_structure": {
    "columns": "1",
    "section_count": 1,
    "ordering": ["top nav", "hero card (eyebrow + H1 over 5 lines + partial subhead)"]
  },
  "buttons_and_links": [
    {"label": "Play", "kind": "button", "primary": false, "x_position": "right", "row_index": 0},
    {"label": "Progress", "kind": "button", "primary": false, "x_position": "right", "row_index": 0}
  ],
  "numbers_dates_amounts": [],
  "table_content": {"present": false, "row_count": 0, "col_count": 0, "header_row": [], "rows": []},
  "glyphs_and_icons": [
    {"in_block": "subhead", "glyph": "—", "shape_description": "em dash"}
  ],
  "uncertain_items": [],
  "below_fold_or_clipped": {
    "appears_clipped": true,
    "evidence": "Subhead is the last visible block, ending mid-paragraph at the bottom edge. CTAs ('Start playing', 'I'm a parent', 'I'm a teacher') are entirely below the fold and not present in the frame.",
    "expected_missing_elements": ["Start playing CTA", "I'm a parent CTA", "I'm a teacher CTA", "No sign-up required", "FOR KIDS section", "FOR PARENTS section", "FOR TEACHERS section", "HOW IT WORKS step grid", "WHY KOMBO comparison table"]
  },
  "interpretation": {
    "semantic_summary": "Stress test at minimum supported viewport — H1 wraps to 5 lines and CTAs are completely below the fold; user would need to scroll before any action is reachable",
    "subjective_notes": ""
  },
  "confidence": {"overall": 0.99, "ocr": 1.0, "color": 0.94, "layout": 0.99}
}
```

## Notes (frontier observations)
- H1 wraps to 5 lines; this is a UX problem (CTAs below the fold).
- This is the dataset's "worst case" viewport — every other shot has CTAs visible.
- Cycle 1 baseline VLM scored this 1/5 on uncertainty (asserted "no issues"). v0.2.2 correctly flags `appears_clipped: true`.
