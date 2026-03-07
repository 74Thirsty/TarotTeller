# Tarot Deck Card Image Specifications (Text-Only)

This directory intentionally stores **text specifications only** in this repository revision.

Design/export one image per card id from `../rider_waite.json`.

## Global spec

- **Title:** Rider-Waite Card Image Set
- **Purpose:** Offline card art used by Tarot Teller reading results.
- **Dimensions:** 512 × 768 px per card (portrait), PNG or WebP.
- **Primary Elements:**
  - Card title region at top.
  - Central illustration area.
  - Optional border/frame motif.
- **Style:** Consistent tarot-inspired visual language across all 78 cards.
- **Text Content:** Card name matching `name` in deck JSON.
- **Notes:** Filename must match `id` field exactly, e.g., `the_fool.png`.

## File mapping rule

For every card entry in `rider_waite.json`:
- output image path: `assets/deck/images/<id>.png`
- example: `id = "two_of_wands"` => `two_of_wands.png`
