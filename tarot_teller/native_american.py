"""Native American medicine wheel insights."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import NamedTuple, Sequence


class _TotemRange(NamedTuple):
    start: tuple[int, int]
    end: tuple[int, int]
    totem: str
    element: str
    clan: str
    keywords: Sequence[str]


_TOTEM_RANGES: list[_TotemRange] = [
    _TotemRange((1, 20), (2, 18), "Otter", "Air", "Butterfly Clan", ("inventive", "supportive", "compassionate")),
    _TotemRange((2, 19), (3, 20), "Wolf", "Water", "Frog Clan", ("romantic", "intuitive", "protective")),
    _TotemRange((3, 21), (4, 19), "Falcon", "Fire", "Hawk Clan", ("sharp-eyed", "strategic", "decisive")),
    _TotemRange((4, 20), (5, 20), "Beaver", "Earth", "Turtle Clan", ("resourceful", "grounded", "collaborative")),
    _TotemRange((5, 21), (6, 20), "Deer", "Air", "Butterfly Clan", ("playful", "inspiring", "quick-witted")),
    _TotemRange((6, 21), (7, 21), "Woodpecker", "Water", "Frog Clan", ("nurturing", "rhythmic", "devoted")),
    _TotemRange((7, 22), (8, 21), "Salmon", "Fire", "Hawk Clan", ("driven", "generous", "creative")),
    _TotemRange((8, 22), (9, 21), "Bear", "Earth", "Turtle Clan", ("practical", "patient", "healing")),
    _TotemRange((9, 22), (10, 22), "Raven", "Air", "Butterfly Clan", ("diplomatic", "visionary", "transformative")),
    _TotemRange((10, 23), (11, 21), "Snake", "Water", "Frog Clan", ("mystical", "adaptable", "catalytic")),
    _TotemRange((11, 22), (12, 21), "Owl", "Fire", "Hawk Clan", ("perceptive", "truth-seeking", "philosophical")),
    _TotemRange((12, 22), (1, 19), "Goose", "Earth", "Turtle Clan", ("ambitious", "enduring", "community-minded")),
]


@dataclass(frozen=True)
class TotemInsight:
    totem: str
    element: str
    clan: str
    keywords: tuple[str, ...]
    message: str


def totem_for(birthdate: date) -> TotemInsight:
    month_day = (birthdate.month, birthdate.day)

    for totem_range in _TOTEM_RANGES:
        if _in_range(month_day, totem_range.start, totem_range.end):
            message = _craft_message(totem_range)
            return TotemInsight(
                totem=totem_range.totem,
                element=totem_range.element,
                clan=totem_range.clan,
                keywords=tuple(totem_range.keywords),
                message=message,
            )

    raise ValueError("No totem range found; check configuration data.")


def _in_range(value: tuple[int, int], start: tuple[int, int], end: tuple[int, int]) -> bool:
    if start <= end:
        return start <= value <= end
    # Handles wrap-around (Goose range across new year).
    return value >= start or value <= end


def _craft_message(totem_range: _TotemRange) -> str:
    qualities = _join_words(totem_range.keywords)
    return (
        f"The {totem_range.totem} walks with you as part of the {totem_range.clan}. "
        f"This medicine wheel position emphasizes {totem_range.element.lower()} element wisdom—"
        f"expect your {qualities} nature to open doors for deeper belonging and reciprocity."
    )


def _join_words(words: Sequence[str]) -> str:
    if not words:
        return ""
    if len(words) == 1:
        return words[0]
    return ", ".join(words[:-1]) + f", and {words[-1]}"
