"""Deterministic reading engine."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable

from .deck import TarotCard
from .rng import build_rng, daily_seed

SPREAD_SIZES = {
    "daily": 1,
    "three_card": 3,
    "yes_no": 1,
    "celtic_cross": 10,
}


@dataclass(frozen=True)
class DrawnCard:
    card: TarotCard
    reversed: bool
    position: str


@dataclass(frozen=True)
class SpreadResult:
    spread: str
    seed: str
    question: str
    cards: list[DrawnCard]


class ReadingEngine:
    def __init__(self, cards: Iterable[TarotCard]):
        self._cards = list(cards)

    def draw(
        self,
        spread: str,
        *,
        include_reversals: bool = True,
        question: str = "",
        seed: str | None = None,
    ) -> SpreadResult:
        if spread not in SPREAD_SIZES:
            raise ValueError(f"Unknown spread: {spread}")

        if spread == "daily":
            final_seed = seed or daily_seed()
        else:
            final_seed = seed or datetime.now(timezone.utc).isoformat()

        rng = build_rng(final_seed)
        count = SPREAD_SIZES[spread]
        if count > len(self._cards):
            raise ValueError("Spread size exceeds deck size")

        selected = rng.sample(self._cards, k=count)
        positions = self._positions_for(spread)
        drawn: list[DrawnCard] = []
        for idx, card in enumerate(selected):
            is_reversed = include_reversals and bool(rng.getrandbits(1))
            drawn.append(DrawnCard(card=card, reversed=is_reversed, position=positions[idx]))

        return SpreadResult(
            spread=spread,
            seed=str(final_seed),
            question=question.strip(),
            cards=drawn,
        )

    @staticmethod
    def _positions_for(spread: str) -> list[str]:
        if spread == "three_card":
            return ["Past", "Present", "Future"]
        if spread == "yes_no":
            return ["Answer"]
        if spread == "celtic_cross":
            return [
                "Present",
                "Challenge",
                "Distant Past",
                "Recent Past",
                "Potential",
                "Near Future",
                "Self",
                "Environment",
                "Hopes/Fears",
                "Outcome",
            ]
        return ["Daily Insight"]
