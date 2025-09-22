"""Tarot card mechanics for TarotTeller."""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Iterable, Sequence


@dataclass(frozen=True)
class TarotCard:
    name: str
    keywords: tuple[str, ...]
    upright: str


@dataclass(frozen=True)
class SpreadCard:
    position: str
    card: TarotCard

    def narrative(self) -> str:
        keyword_phrase = _join_keywords(self.card.keywords)
        return (
            f"{self.position}: {self.card.name} ({keyword_phrase}). {self.card.upright}"
        )


@dataclass(frozen=True)
class TarotReading:
    spread: tuple[SpreadCard, ...]

    def summary(self) -> str:
        lines = [entry.narrative() for entry in self.spread]
        return "\n".join(lines)


def draw_three_card_spread(rng: random.Random | None = None) -> TarotReading:
    rng = rng or random.Random()
    cards = rng.sample(_MAJOR_ARCANA, 3)
    positions = ("Past", "Present", "Future")
    spread = tuple(SpreadCard(position, card) for position, card in zip(positions, cards))
    return TarotReading(spread=spread)


_MAJOR_ARCANA: Sequence[TarotCard] = (
    TarotCard("The Fool", ("beginnings", "spontaneity", "faith"), "A leap into the unknown invites sacred trust."),
    TarotCard("The Magician", ("manifestation", "skill", "willpower"), "You already possess the tools required to shape this moment."),
    TarotCard("The High Priestess", ("intuition", "mystery", "inner voice"), "Listen for the whispers beneath surface logic."),
    TarotCard("The Empress", ("fertility", "sensuality", "abundance"), "Nurture your ideas the way you would a flourishing garden."),
    TarotCard("The Emperor", ("structure", "authority", "stability"), "Disciplined action turns inspiration into legacy."),
    TarotCard("The Hierophant", ("tradition", "wisdom", "mentorship"), "Ritual and shared wisdom anchor your next steps."),
    TarotCard("The Lovers", ("alignment", "connection", "values"), "Choose what mirrors your heart's deepest truth."),
    TarotCard("The Chariot", ("determination", "focus", "momentum"), "Harness contrasting forces to drive forward with grace."),
    TarotCard("Strength", ("courage", "compassion", "resilience"), "Gentle strength outshines brute force now."),
    TarotCard("The Hermit", ("solitude", "searching", "inner guidance"), "Illuminate the path by honoring reflective pauses."),
    TarotCard("Wheel of Fortune", ("cycles", "destiny", "turning point"), "Change is the only constant—pivot with intention."),
    TarotCard("Justice", ("equilibrium", "truth", "accountability"), "Seek balance by aligning actions with integrity."),
    TarotCard("The Hanged One", ("surrender", "perspective", "pause"), "Stillness births the revelation you seek."),
    TarotCard("Death", ("release", "transformation", "rebirth"), "Letting go clears space for extraordinary renewal."),
    TarotCard("Temperance", ("alchemy", "moderation", "purpose"), "Blend disparate pieces of your life into a cohesive whole."),
    TarotCard("The Devil", ("shadow", "attachment", "awakening"), "Liberation arrives when you name the chains you carry."),
    TarotCard("The Tower", ("revelation", "upheaval", "liberation"), "Radical truth dismantles what was never stable."),
    TarotCard("The Star", ("hope", "healing", "inspiration"), "Your vulnerability is a lighthouse for others."),
    TarotCard("The Moon", ("dreams", "intuition", "subconscious"), "Honor cyclical emotions—they are sacred navigation tools."),
    TarotCard("The Sun", ("vitality", "joy", "radiance"), "Your authenticity is magnetic—let it shine freely."),
    TarotCard("Judgement", ("awakening", "forgiveness", "purpose"), "Answer the call that won't stop echoing in your soul."),
    TarotCard("The World", ("completion", "integration", "wholeness"), "Celebrate how far you've traveled and claim the next horizon."),
)


def _join_keywords(keywords: Iterable[str]) -> str:
    keywords = tuple(keywords)
    if not keywords:
        return ""
    if len(keywords) == 1:
        return keywords[0]
    return ", ".join(keywords[:-1]) + f", and {keywords[-1]}"
