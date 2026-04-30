# Opus 4.7 Ground Truth — 01_desktop_hero.png

**viewport:** 1440×900 desktop
**section:** Top nav + hero card + start of FOR KIDS card
**analyst:** Claude Opus 4.7 (frontier vision)

```json
{
  "image_type": "webpage_screenshot",
  "viewport_class": "desktop",
  "visible_text": [
    {"block_id": "nav_logo", "role": "nav", "text": "kombo", "x_position": "left", "color_descriptor": "near-black", "weight": "bold"},
    {"block_id": "nav_play", "role": "nav", "text": "Play", "x_position": "right", "color_descriptor": "near-black", "weight": "regular"},
    {"block_id": "nav_progress", "role": "nav", "text": "Progress", "x_position": "right", "color_descriptor": "near-black", "weight": "regular"},
    {"block_id": "eyebrow", "role": "eyebrow", "text": "READY TO PLAY", "x_position": "left", "color_descriptor": "purple", "weight": "regular"},
    {"block_id": "h1", "role": "heading_h1", "text": "The math RPG where you build a kingdom", "x_position": "left", "color_descriptor": "near-black", "weight": "bold"},
    {"block_id": "subhead", "role": "body", "text": "Practice multiplication and division, earn sparks, and grow your kingdom — one kombo at a time.", "x_position": "left", "color_descriptor": "muted-grey", "weight": "regular"},
    {"block_id": "cta_primary", "role": "button_label", "text": "Start playing", "x_position": "left", "color_descriptor": "near-black", "weight": "regular"},
    {"block_id": "cta_parent", "role": "button_label", "text": "I'm a parent", "x_position": "left", "color_descriptor": "near-black", "weight": "regular"},
    {"block_id": "cta_teacher", "role": "button_label", "text": "I'm a teacher", "x_position": "left", "color_descriptor": "near-black", "weight": "regular"},
    {"block_id": "no_signup", "role": "body", "text": "No sign-up required", "x_position": "left", "color_descriptor": "muted-grey", "weight": "regular"},
    {"block_id": "kids_eyebrow", "role": "eyebrow", "text": "FOR KIDS", "x_position": "left", "color_descriptor": "purple", "weight": "regular"},
    {"block_id": "kids_heading", "role": "heading_h2", "text": "Not a test — an adventure", "x_position": "left", "color_descriptor": "near-black", "weight": "bold"},
    {"block_id": "kids_body", "role": "body", "text": "Solve math problems to earn sparks. Use sparks to build your kingdom. Each correct answer makes your world bigger.", "x_position": "left", "color_descriptor": "muted-grey", "weight": "regular"},
    {"block_id": "parents_eyebrow", "role": "eyebrow", "text": "FOR PARENTS", "x_position": "left", "color_descriptor": "purple", "weight": "regular"},
    {"block_id": "parents_heading", "role": "heading_h2", "text": "Math practice without the nagging", "x_position": "left", "color_descriptor": "near-black", "weight": "bold"}
  ],
  "key_ui_elements": [
    {"kind": "button", "label": "Start playing", "notes": "primary CTA, solid purple pill, near-black text"},
    {"kind": "button", "label": "I'm a parent", "notes": "secondary, white pill with light grey border"},
    {"kind": "button", "label": "I'm a teacher", "notes": "secondary, white pill with light grey border"},
    {"kind": "button", "label": "Play", "notes": "nav pill, white background"},
    {"kind": "button", "label": "Progress", "notes": "nav pill, white background"},
    {"kind": "illustration", "label": "purple egg", "notes": "solid purple oval/egg shape on right side of hero, decorative"}
  ],
  "layout_structure": {
    "columns": "1 (text-left, decoration-right within hero)",
    "section_count": 3,
    "ordering": ["top nav", "hero card", "FOR KIDS card (full)", "FOR PARENTS card (heading only, body clipped)"]
  },
  "buttons_and_links": [
    {"label": "Play", "kind": "button", "primary": false, "x_position": "right", "row_index": 0},
    {"label": "Progress", "kind": "button", "primary": false, "x_position": "right", "row_index": 0},
    {"label": "Start playing", "kind": "button", "primary": true, "x_position": "left", "row_index": 1},
    {"label": "I'm a parent", "kind": "button", "primary": false, "x_position": "left", "row_index": 1},
    {"label": "I'm a teacher", "kind": "button", "primary": false, "x_position": "left", "row_index": 1}
  ],
  "numbers_dates_amounts": [],
  "table_content": {"present": false, "row_count": 0, "col_count": 0, "header_row": [], "rows": []},
  "glyphs_and_icons": [
    {"in_block": "subhead", "glyph": "—", "shape_description": "em dash", "preceding_text": "your kingdom", "following_text": "one kombo at a time"},
    {"in_block": "kids_heading", "glyph": "—", "shape_description": "em dash", "preceding_text": "Not a test", "following_text": "an adventure"}
  ],
  "uncertain_items": [],
  "below_fold_or_clipped": {
    "appears_clipped": true,
    "evidence": "FOR PARENTS card only shows eyebrow + heading; body and waitlist link clipped at bottom edge",
    "expected_missing_elements": ["FOR PARENTS body paragraph", "Join the parent waitlist link", "FOR TEACHERS section", "HOW IT WORKS section", "comparison table"]
  },
  "interpretation": {
    "semantic_summary": "Marketing landing for kombo, a math practice RPG; hero pitches three audience CTAs",
    "subjective_notes": ""
  },
  "confidence": {"overall": 0.99, "ocr": 1.0, "color": 0.95, "layout": 0.99}
}
```

## Notes (frontier observations)
- Background of hero/cards is a very pale lavender tint (`#F4F0FA`-ish), not white — local VLM rarely picks this up.
- "Start playing" sits on a solid medium-purple pill (`#7C3AED`-ish); the *text* is dark, not white as the v0.2.2 structured run claimed.
- The egg shape is a single solid purple shape with a subtle gloss highlight, not multiple shapes.
- Three CTAs are all on one row; baseline VLM in cycle 1 sometimes claimed "centered".
