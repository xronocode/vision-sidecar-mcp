# Opus 4.7 Ground Truth — 05_tablet_portrait_hero.png

**viewport:** 768×1024 tablet portrait
**section:** Top nav + hero card + FOR KIDS card + start of FOR PARENTS card (with waitlist link visible)
**analyst:** Claude Opus 4.7 (frontier vision)

```json
{
  "image_type": "webpage_screenshot",
  "viewport_class": "tablet",
  "visible_text": [
    {"block_id": "nav_logo", "role": "nav", "text": "kombo", "x_position": "left", "color_descriptor": "near-black", "weight": "bold"},
    {"block_id": "nav_play", "role": "nav", "text": "Play", "x_position": "right", "color_descriptor": "near-black", "weight": "regular"},
    {"block_id": "nav_progress", "role": "nav", "text": "Progress", "x_position": "right", "color_descriptor": "near-black", "weight": "regular"},
    {"block_id": "eyebrow", "role": "eyebrow", "text": "READY TO PLAY", "x_position": "left", "color_descriptor": "purple", "weight": "regular"},
    {"block_id": "h1_l1", "role": "heading_h1", "text": "The math RPG where", "x_position": "left", "color_descriptor": "near-black", "weight": "bold"},
    {"block_id": "h1_l2", "role": "heading_h1", "text": "you build a kingdom", "x_position": "left", "color_descriptor": "near-black", "weight": "bold"},
    {"block_id": "subhead", "role": "body", "text": "Practice multiplication and division, earn sparks, and grow your kingdom — one kombo at a time.", "x_position": "left", "color_descriptor": "muted-grey", "weight": "regular"},
    {"block_id": "cta_primary", "role": "button_label", "text": "Start playing", "x_position": "left", "color_descriptor": "near-black", "weight": "regular"},
    {"block_id": "cta_parent", "role": "button_label", "text": "I'm a parent", "x_position": "left", "color_descriptor": "near-black", "weight": "regular"},
    {"block_id": "cta_teacher", "role": "button_label", "text": "I'm a teacher", "x_position": "left", "color_descriptor": "near-black", "weight": "regular"},
    {"block_id": "no_signup", "role": "body", "text": "No sign-up required", "x_position": "left", "color_descriptor": "muted-grey", "weight": "regular"},
    {"block_id": "kids_eyebrow", "role": "eyebrow", "text": "FOR KIDS", "x_position": "left", "color_descriptor": "purple", "weight": "regular"},
    {"block_id": "kids_heading", "role": "heading_h2", "text": "Not a test — an adventure", "x_position": "left", "color_descriptor": "near-black", "weight": "bold"},
    {"block_id": "kids_body", "role": "body", "text": "Solve math problems to earn sparks. Use sparks to build your kingdom. Each correct answer makes your world bigger.", "x_position": "left", "color_descriptor": "muted-grey", "weight": "regular"},
    {"block_id": "parents_eyebrow", "role": "eyebrow", "text": "FOR PARENTS", "x_position": "left", "color_descriptor": "purple", "weight": "regular"},
    {"block_id": "parents_heading", "role": "heading_h2", "text": "Math practice without the nagging", "x_position": "left", "color_descriptor": "near-black", "weight": "bold"},
    {"block_id": "parents_body", "role": "body", "text": "A parent dashboard is on the way. See progress, set goals, and stay informed — without turning into homework police.", "x_position": "left", "color_descriptor": "muted-grey", "weight": "regular"},
    {"block_id": "parents_link", "role": "link", "text": "Join the parent waitlist →", "x_position": "left", "color_descriptor": "purple", "weight": "bold"}
  ],
  "key_ui_elements": [
    {"kind": "button", "label": "Start playing", "notes": "primary CTA, solid purple pill"},
    {"kind": "button", "label": "I'm a parent", "notes": "secondary, white pill"},
    {"kind": "button", "label": "I'm a teacher", "notes": "secondary, white pill"},
    {"kind": "button", "label": "Play", "notes": "nav pill"},
    {"kind": "button", "label": "Progress", "notes": "nav pill"},
    {"kind": "link", "label": "Join the parent waitlist →", "notes": "purple text"}
  ],
  "layout_structure": {
    "columns": "1 (single-column tablet layout; egg illustration hidden by responsive rules)",
    "section_count": 3,
    "ordering": ["top nav", "hero card (no decorative egg)", "FOR KIDS card", "FOR PARENTS card (full)"]
  },
  "buttons_and_links": [
    {"label": "Play", "kind": "button", "primary": false, "x_position": "right", "row_index": 0},
    {"label": "Progress", "kind": "button", "primary": false, "x_position": "right", "row_index": 0},
    {"label": "Start playing", "kind": "button", "primary": true, "x_position": "left", "row_index": 1},
    {"label": "I'm a parent", "kind": "button", "primary": false, "x_position": "left", "row_index": 1},
    {"label": "I'm a teacher", "kind": "button", "primary": false, "x_position": "left", "row_index": 1},
    {"label": "Join the parent waitlist →", "kind": "link", "primary": false, "x_position": "left", "row_index": 3}
  ],
  "numbers_dates_amounts": [],
  "table_content": {"present": false, "row_count": 0, "col_count": 0, "header_row": [], "rows": []},
  "glyphs_and_icons": [
    {"in_block": "subhead", "glyph": "—", "shape_description": "em dash"},
    {"in_block": "kids_heading", "glyph": "—", "shape_description": "em dash"},
    {"in_block": "parents_body", "glyph": "—", "shape_description": "em dash"},
    {"in_block": "parents_link", "glyph": "→", "shape_description": "right arrow"}
  ],
  "uncertain_items": [],
  "below_fold_or_clipped": {
    "appears_clipped": true,
    "evidence": "FOR TEACHERS card and HOW IT WORKS section not visible below the fold",
    "expected_missing_elements": ["FOR TEACHERS section", "HOW IT WORKS step grid", "WHY KOMBO comparison table"]
  },
  "interpretation": {
    "semantic_summary": "Tablet portrait rendering of the marketing landing — egg decoration dropped, headline wraps to two lines, CTAs all on one row",
    "subjective_notes": ""
  },
  "confidence": {"overall": 0.99, "ocr": 1.0, "color": 0.94, "layout": 0.99}
}
```

## Notes (frontier observations)
- H1 wraps to exactly 2 lines at 768px ("The math RPG where" / "you build a kingdom").
- All three CTAs still fit on one row at this width.
- Egg illustration is gone (responsive rule hides it below ~1024px).
