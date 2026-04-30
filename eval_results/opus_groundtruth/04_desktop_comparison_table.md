# Opus 4.7 Ground Truth — 04_desktop_comparison_table.png

**viewport:** 1440×900 desktop
**section:** byte-identical to 03_desktop_how_it_works.png — see metadata.json. Same content visible.
**analyst:** Claude Opus 4.7 (frontier vision)

This file is byte-identical (same MD5 `a444572cb759b0b68bebcf7a8bec8958`) to `03_desktop_how_it_works.png` because at 1440×900 the document is only 1873px tall, so the page bottoms out at scrollY=973 and both target sections appear together.

**Refer to `01_desktop_hero.md` for hero metadata, and `03_desktop_how_it_works.md` for the full structured analysis** — they are the same pixels.

## Frontier note for downstream consumers
This duplication is a property of the dataset capture (documented in metadata.json), not a model failure. A frontier evaluator should:
- Recognize the duplicate from pixel identity, OR
- Note "table is the dominant element below the fold" since the request was scoped to the table.

The structured ground truth identical to file 03 includes:
- Full WHY KOMBO comparison table (4 rows × 3 cols, all cells correct)
- HOW IT WORKS step grid (4 cards with distinct pastel backgrounds)
- FOR TEACHERS card with grey-toned eyebrow

See `03_desktop_how_it_works.md` for the JSON.
