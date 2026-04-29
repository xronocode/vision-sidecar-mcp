# MCP Vision (qwen3-vl:8b, tuned v0.2.0) — Structured (analyze_structured) — 01_desktop_hero.png

**viewport_hint passed:** `desktop`
**preprocess:** `{"original_size": [1440, 900], "upscaled": false}`
**parse_error:** None
**wall_seconds:** 26.11

---

## Parsed JSON result

```json
{
  "image_type": "webpage_screenshot",
  "viewport_class": "desktop",
  "visible_text": [
    {
      "block_id": "top_left",
      "role": "nav",
      "text": "kombo",
      "x_position": "left",
      "color_descriptor": "dark grey",
      "weight": "regular"
    },
    {
      "block_id": "top_right",
      "role": "nav",
      "text": "Play",
      "x_position": "right",
      "color_descriptor": "dark grey",
      "weight": "regular"
    },
    {
      "block_id": "top_right_2",
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
      "x_position": "left",
      "color_descriptor": "light purple",
      "weight": "regular"
    },
    {
      "block_id": "h1",
      "role": "heading_h1",
      "text": "The math RPG where you build a kingdom",
      "x_position": "left",
      "color_descriptor": "dark grey",
      "weight": "bold"
    },
    {
      "block_id": "body_1",
      "role": "body",
      "text": "Practice multiplication and division, earn sparks, and grow your kingdom — one kombo at a time.",
      "x_position": "left",
      "color_descriptor": "dark grey",
      "weight": "regular"
    },
    {
      "block_id": "button_1",
      "role": "button_label",
      "text": "Start playing",
      "x_position": "left",
      "color_descriptor": "white",
      "weight": "regular"
    },
    {
      "block_id": "button_2",
      "role": "button_label",
      "text": "I'm a parent",
      "x_position": "center",
      "color_descriptor": "dark grey",
      "weight": "regular"
    },
    {
      "block_id": "button_3",
      "role": "button_label",
      "text": "I'm a teacher",
      "x_position": "right",
      "color_descriptor": "dark grey",
      "weight": "regular"
    },
    {
      "block_id": "subtext",
      "role": "body",
      "text": "No sign-up required",
      "x_position": "left",
      "color_descriptor": "dark grey",
      "weight": "regular"
    },
    {
      "block_id": "h2_1",
      "role": "heading_h2",
      "text": "FOR KIDS",
      "x_position": "left",
      "color_descriptor": "light purple",
      "weight": "regular"
    },
    {
      "block_id": "h2_2",
      "role": "heading_h2",
      "text": "Not a test — an adventure",
      "x_position": "left",
      "color_descriptor": "dark grey",
      "weight": "bold"
    },
    {
      "block_id": "body_2",
      "role": "body",
      "text": "Solve math problems to earn sparks. Use sparks to build your kingdom. Each correct answer makes your world bigger.",
      "x_position": "left",
      "color_descriptor": "dark grey",
      "weight": "regular"
    },
    {
      "block_id": "h2_3",
      "role": "heading_h2",
      "text": "FOR PARENTS",
      "x_position": "left",
      "color_descriptor": "light purple",
      "weight": "regular"
    },
    {
      "block_id": "h2_4",
      "role": "heading_h2",
      "text": "Math practice without the nagging",
      "x_position": "left",
      "color_descriptor": "dark grey",
      "weight": "bold"
    }
  ],
  "key_ui_elements": [
    {
      "kind": "button",
      "label": "Start playing",
      "notes": "Purple background, rounded corners, white text"
    },
    {
      "kind": "button",
      "label": "I'm a parent",
      "notes": "White background, rounded corners, dark grey text"
    },
    {
      "kind": "button",
      "label": "I'm a teacher",
      "notes": "White background, rounded corners, dark grey text"
    },
    {
      "kind": "icon",
      "label": "Purple oval shape",
      "notes": "Located to the right of the main heading"
    }
  ],
  "layout_structure": {
    "columns": "2",
    "section_count": 3,
    "ordering": [
      "hero section",
      "for kids section",
      "for parents section"
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
      "x_position": "center",
      "row_index": 1
    },
    {
      "label": "I'm a teacher",
      "kind": "button",
      "primary": false,
      "x_position": "right",
      "row_index": 1
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
      "in_block": "body_1",
      "glyph": "—",
      "shape_description": "em dash",
      "preceding_text": "grow your",
      "following_text": "one kombo at a time."
    }
  ],
  "uncertain_items": [],
  "below_fold_or_clipped": {
    "appears_clipped": true,
    "evidence": "The 'FOR PARENTS' section is partially visible with text cut off at the bottom",
    "expected_missing_elements": [
      "Math practice without the nagging",
      "additional content below"
    ]
  },
  "interpretation": {
    "semantic_summary": "A webpage for an educational math game with sections for kids and parents",
    "subjective_notes": ""
  },
  "confidence": {
    "overall": 0.95,
    "ocr": 0.98,
    "color": 0.9,
    "layout": 0.9
  }
}
```
