"""Offline deck loading with cache."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = {
    "id",
    "name",
    "arcana",
    "suit",
    "number",
    "keywords_upright",
    "keywords_reversed",
    "meaning_upright_short",
    "meaning_reversed_short",
    "meaning_upright_long",
    "meaning_reversed_long",
}


@dataclass(frozen=True)
class TarotCard:
    id: str
    name: str
    arcana: str
    suit: str
    number: int
    keywords_upright: list[str]
    keywords_reversed: list[str]
    meaning_upright_short: str
    meaning_reversed_short: str
    meaning_upright_long: str
    meaning_reversed_long: str


class DeckCache:
    """Simple in-process cache for deck payloads."""

    _cards: list[TarotCard] | None = None

    @classmethod
    def get(cls, deck_path: Path) -> list[TarotCard]:
        if cls._cards is None:
            cls._cards = load_deck(deck_path)
        return cls._cards


def load_deck(deck_path: Path) -> list[TarotCard]:
    payload: list[dict[str, Any]] = json.loads(deck_path.read_text(encoding="utf-8"))
    cards: list[TarotCard] = []
    for entry in payload:
        missing = REQUIRED_FIELDS.difference(entry)
        if missing:
            raise ValueError(f"Card missing required fields: {sorted(missing)}")
        cards.append(TarotCard(**entry))
    return cards
