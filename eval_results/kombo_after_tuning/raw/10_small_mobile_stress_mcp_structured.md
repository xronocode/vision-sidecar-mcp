# MCP Vision (qwen3-vl:8b, tuned v0.2.0) — Structured (analyze_structured) — 10_small_mobile_stress.png

**viewport_hint passed:** `small_mobile`
**preprocess:** `{"original_size": [320, 568], "upscaled": true, "factor": 2, "new_size": [640, 1136], "method": "Lanczos"}`
**parse_error:** None
**wall_seconds:** 31.62

---

## Parsed JSON result

```json
{
  "image_type": "mobile_screenshot",
  "viewport_class": "small_mobile",
  "visible_text": [
    {
      "block_id": "top_nav",
      "role": "nav",
      "text": "kombo",
      "x_position": "left",
      "color_descriptor": "dark grey",
      "weight": "regular"
    },
    {
      "block_id": "top_nav_play",
      "role": "button_label",
      "text": "Play",
      "x_position": "center",
      "color_descriptor": "dark grey",
      "weight": "regular"
    },
    {
      "block_id": "top_nav_progress",
      "role": "button_label",
      "text": "Progress",
      "x_position": "center",
      "color_descriptor": "dark grey",
      "weight": "regular"
    },
    {
      "block_id": "eyebrow",
      "role": "eyebrow",
      "text": "READY TO PLAY",
      "x_position": "center",
      "color_descriptor": "purple",
      "weight": "regular"
    },
    {
      "block_id": "hero_heading",
      "role": "heading_h1",
      "text": "The math RPG where you build a kingdom",
      "x_position": "center",
      "color_descriptor": "dark grey",
      "weight": "bold"
    },
    {
      "block_id": "hero_subhead",
      "role": "body",
      "text": "Practice multiplication and division, earn sparks, and grow your kingdom — one kombo at a time.",
      "x_position": "center",
      "color_descriptor": "muted grey",
      "weight": "regular"
    }
  ],
  "key_ui_elements": [
    {
      "kind": "top navigation bar",
      "label": "kombo, Play, Progress",
      "notes": "Navigation bar with brand name and two buttons"
    },
    {
      "kind": "hero section",
      "label": "READY TO PLAY, The math RPG where you build a kingdom",
      "notes": "Main heading and subheading"
    }
  ],
  "layout_structure": {
    "columns": "1",
    "section_count": 2,
    "ordering": [
      "top navigation bar",
      "hero section"
    ]
  },
  "buttons_and_links": [
    {
      "label": "Play",
      "kind": "button",
      "primary": false,
      "x_position": "center",
      "row_index": 0
    },
    {
      "label": "Progress",
      "kind": "button",
      "primary": false,
      "x_position": "center",
      "row_index": 0
    }
  ],
  "numbers_dates_amounts": [],
  "table_content": {
    "present": false,
    "row_count": 0,
    "col_count": 0,
    "header_row": [],
    "rows": []
  },
  "glyphs_and_icons": [
    {
      "in_block": "hero_subhead",
      "glyph": "—",
      "shape_description": "en dash",
      "preceding_text": "grow your kingdom",
      "following_text": "one kombo at a time."
    }
  ],
  "uncertain_items": [],
  "below_fold_or_clipped": {
    "appears_clipped": true,
    "evidence": "Hero section has heading and subhead but no primary action button below subhead",
    "expected_missing_elements": [
      "primary action button (e.g. 'Start playing', 'Get started', 'Sign up')"
    ]
  },
  "interpretation": {
    "semantic_summary": "Mobile screenshot of a game's hero section with navigation bar and descriptive text",
    "subjective_notes": null
  },
  "confidence": {
    "overall": 0.95,
    "ocr": 0.98,
    "color": 0.95,
    "layout": 0.9
  }
}
```
