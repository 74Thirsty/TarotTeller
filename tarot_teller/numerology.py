"""Chaldean numerology helpers."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import unicodedata


_CHALDEAN_MAP = {
    "A": 1,
    "I": 1,
    "J": 1,
    "Q": 1,
    "Y": 1,
    "B": 2,
    "K": 2,
    "R": 2,
    "C": 3,
    "G": 3,
    "L": 3,
    "S": 3,
    "D": 4,
    "M": 4,
    "T": 4,
    "E": 5,
    "H": 5,
    "N": 5,
    "X": 5,
    "U": 6,
    "V": 6,
    "W": 6,
    "O": 7,
    "Z": 7,
    "F": 8,
    "P": 8,
}

_MASTER_NUMBERS = {11, 22}

_NAME_MEANINGS = {
    1: "Leadership, pioneering spirit, and the courage to forge your own path.",
    2: "Diplomacy, empathy, and the gift of weaving people together.",
    3: "Creative expression, optimism, and the joy of storytelling.",
    4: "Steadfast structure, reliability, and craftsmanship in all pursuits.",
    5: "Adventure, adaptability, and a restless hunger for experience.",
    6: "Nurturing guardianship, harmony, and heart-centered responsibility.",
    7: "Mysticism, introspection, and the pursuit of deeper truths.",
    8: "Manifestation, executive power, and wise stewardship of resources.",
    11: "Visionary insight and the ability to illuminate the collective imagination.",
    22: "Master builder energy capable of turning bold ideals into reality.",
}

_BIRTH_MEANINGS = {
    1: "You thrive when taking initiative and trusting your instincts.",
    2: "Your life path is enriched through cooperation and attentive listening.",
    3: "You flourish by communicating, teaching, and inspiring.",
    4: "Consistent effort and grounded planning are your superpowers.",
    5: "Freedom and variety keep your spirit animated—keep exploring.",
    6: "Service and community caretaking bring you soulful satisfaction.",
    7: "Quiet study, contemplation, and spiritual inquiry recharge you.",
    8: "You are learning to balance ambition with integrity and generosity.",
    9: "Your path asks for compassion, artistic contribution, and letting go.",
    11: "You are tuned to synchronicity—share your intuitive downloads.",
    22: "Architect your visions with patience; they can uplift many.",
}


@dataclass(frozen=True)
class NumerologyInsight:
    name_number: int
    birth_number: int
    name_breakdown: tuple[tuple[str, int], ...]
    summary: str


def chaldean_numerology_for(name: str, birthdate: date) -> NumerologyInsight:
    cleaned = _normalize_name(name)
    breakdown: list[tuple[str, int]] = []
    total = 0
    for char in cleaned:
        value = _CHALDEAN_MAP.get(char)
        if value is None:
            continue
        breakdown.append((char, value))
        total += value

    name_number = _reduce_number(total)
    birth_number = _reduce_number(sum(int(digit) for digit in birthdate.strftime("%Y%m%d")))

    summary = _summarize(name_number, birth_number)

    return NumerologyInsight(
        name_number=name_number,
        birth_number=birth_number,
        name_breakdown=tuple(breakdown),
        summary=summary,
    )


def _normalize_name(name: str) -> str:
    normalized = unicodedata.normalize("NFKD", name)
    return "".join(c for c in normalized.upper() if c.isalpha())


def _reduce_number(value: int) -> int:
    while value not in _MASTER_NUMBERS and value >= 10:
        value = sum(int(digit) for digit in str(value))
    return value


def _summarize(name_number: int, birth_number: int) -> str:
    name_meaning = _NAME_MEANINGS.get(name_number)
    birth_meaning = _BIRTH_MEANINGS.get(birth_number)

    parts: list[str] = []
    if name_meaning:
        parts.append(
            f"Your Chaldean name number is {name_number}, highlighting {name_meaning}"
        )
    else:
        parts.append(
            "Your Chaldean name number carries a unique vibration beyond the traditional canon."
        )

    if birth_meaning:
        parts.append(f"Your birth number {birth_number} suggests {birth_meaning}")
    else:
        parts.append(
            "Your birth number adds an unconventional rhythm—trust the path unfolding before you."
        )

    return " ".join(parts)
