#!/usr/bin/env python3
"""Validate tarot card image coverage against the deck JSON."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECK_JSON = ROOT / "tarot_teller_android" / "app" / "assets" / "deck" / "rider_waite.json"
IMAGE_DIR = ROOT / "tarot_teller_android" / "app" / "assets" / "deck" / "images"


def main() -> int:
    cards = json.loads(DECK_JSON.read_text(encoding="utf-8"))
    card_ids = {entry["id"] for entry in cards}
    image_ids = {path.stem for path in IMAGE_DIR.glob("*.png")}

    missing = sorted(card_ids - image_ids)
    if missing:
        print("Missing card images:")
        for card_id in missing:
            print(f" - {card_id}")
        return 1

    print(f"OK: {len(card_ids)} card IDs have matching images in {IMAGE_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
