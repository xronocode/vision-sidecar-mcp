# MCP Vision (qwen3-vl:8b, tuned v0.2.0) — Structured (analyze_structured) — 07_mobile_hero.png

**viewport_hint passed:** `mobile`
**preprocess:** `{"original_size": [390, 844], "upscaled": true, "factor": 2, "new_size": [780, 1688], "method": "Lanczos"}`
**parse_error:** None
**wall_seconds:** 29.08

---

## Parsed JSON result

```json
{
  "image_type": "mobile_screenshot",
  "viewport_class": "mobile",
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
      "role": "nav",
      "text": "Play",
      "x_position": "center",
      "color_descriptor": "dark grey",
      "weight": "regular"
    },
    {
      "block_id": "top_nav_progress",
      "role": "nav",
      "text": "Progress",
      "x_position": "right",
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
      "block_id": "h1",
      "role": "heading_h1",
      "text": "The math RPG where you build a kingdom",
      "x_position": "center",
      "color_descriptor": "dark grey",
      "weight": "bold"
    },
    {
      "block_id": "body",
      "role": "body",
      "text": "Practice multiplication and division, earn sparks, and grow your kingdom — one kombo at a time.",
      "x_position": "center",
      "color_descriptor": "muted grey",
      "weight": "regular"
    },
    {
      "block_id": "button_start",
      "role": "button_label",
      "text": "Start playing",
      "x_position": "left",
      "color_descriptor": "white",
      "weight": "regular"
    },
    {
      "block_id": "button_parent",
      "role": "button_label",
      "text": "I'm a parent",
      "x_position": "right",
      "color_descriptor": "dark grey",
      "weight": "regular"
    },
    {
      "block_id": "button_teacher",
      "role": "button_label",
      "text": "I'm a teacher",
      "x_position": "left",
      "color_descriptor": "dark grey",
      "weight": "regular"
    },
    {
      "block_id": "footer_text",
      "role": "body",
      "text": "No sign-up required",
      "x_position": "center",
      "color_descriptor": "muted grey",
      "weight": "regular"
    },
    {
      "block_id": "h2",
      "role": "heading_h2",
      "text": "FOR KIDS",
      "x_position": "center",
      "color_descriptor": "purple",
      "weight": "regular"
    },
    {
      "block_id": "h3",
      "role": "heading_h3",
      "text": "Not a test — an adventure",
      "x_position": "center",
      "color_descriptor": "dark grey",
      "weight": "bold"
    }
  ],
  "key_ui_elements": [
    {
      "kind": "button",
      "label": "Start playing",
      "notes": "Purple background, rounded corners, centered text"
    },
    {
      "kind": "button",
      "label": "I'm a parent",
      "notes": "White background, rounded corners, centered text"
    },
    {
      "kind": "button",
      "label": "I'm a teacher",
      "notes": "White background, rounded corners, centered text"
    },
    {
      "kind": "nav",
      "label": "Play",
      "notes": "Rounded button, white background, centered text"
    },
    {
      "kind": "nav",
      "label": "Progress",
      "notes": "Rounded button, white background, centered text"
    }
  ],
  "layout_structure": {
    "columns": "1",
    "section_count": 3,
    "ordering": [
      "top_nav",
      "hero_section",
      "cta_section",
      "footer_section"
    ]
  },
  "buttons_and_links": [
    {
      "label": "Start playing",
      "kind": "button",
      "primary": true,
      "x_position": "left",
      "row_index": 1
    },
    {
      "label": "I'm a parent",
      "kind": "button",
      "primary": false,
      "x_position": "right",
      "row_index": 1
    },
    {
      "label": "I'm a teacher",
      "kind": "button",
      "primary": false,
      "x_position": "left",
      "row_index": 2
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
      "in_block": "body",
      "glyph": "—",
      "shape_description": "em dash",
      "preceding_text": "grow your kingdom",
      "following_text": "one kombo at a time."
    }
  ],
  "uncertain_items": [
    {
      "block_id": "h3",
      "concern": "Text appears partially visible at bottom of viewport"
    }
  ],
  "below_fold_or_clipped": {
    "appears_clipped": true,
    "evidence": "Text 'Not a test — an adventure' is visible but appears to be cut off at the bottom of the viewport",
    "expected_missing_elements": [
      "'Solve math problems to earn sparks'"
    ]
  },
  "interpretation": {
    "semantic_summary": "A mobile app screen for 'kombo' featuring a game description and user role selection buttons",
    "subjective_notes": ""
  },
  "confidence": {
    "overall": 0.95,
    "ocr": 0.98,
    "color": 0.95,
    "layout": 0.9
  }
}
```
