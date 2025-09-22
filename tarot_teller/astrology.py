"""Astrological insights for TarotTeller."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class ZodiacInsight:
    sign: str
    element: str
    ruling_planet: str
    summary: str


_ZODIAC_DATA = [
    ((1, 20), "Aquarius", "Air", "Saturn & Uranus", "The visionary water bearer balancing intellect with humanitarian heart."),
    ((2, 19), "Pisces", "Water", "Jupiter & Neptune", "An empathic dreamer guided by intuition and compassionate creativity."),
    ((3, 21), "Aries", "Fire", "Mars", "A courageous spark ready to initiate bold adventures."),
    ((4, 20), "Taurus", "Earth", "Venus", "A steady soul who cultivates beauty, comfort, and tangible progress."),
    ((5, 21), "Gemini", "Air", "Mercury", "A quicksilver messenger weaving curiosity into insight."),
    ((6, 21), "Cancer", "Water", "Moon", "A lunar nurturer protecting emotional truth and chosen family."),
    ((7, 23), "Leo", "Fire", "Sun", "A radiant heart-leader who shines through generosity and creativity."),
    ((8, 23), "Virgo", "Earth", "Mercury", "An intuitive analyst harmonizing practicality with mindful service."),
    ((9, 23), "Libra", "Air", "Venus", "A diplomatic balancer seeking harmony, justice, and aesthetic grace."),
    ((10, 23), "Scorpio", "Water", "Mars & Pluto", "A mystic alchemist transforming through depth and devotion."),
    ((11, 22), "Sagittarius", "Fire", "Jupiter", "An expansive truth-seeker roaming between wisdom and wonder."),
    ((12, 22), "Capricorn", "Earth", "Saturn", "A mountain climber crafting legacy through discipline and heart."),
]


def western_zodiac_for(birthdate: date) -> ZodiacInsight:
    """Return the western zodiac insight for ``birthdate``."""

    month_day = (birthdate.month, birthdate.day)
    insight_data = _ZODIAC_DATA[-1]
    for index, (start, sign, element, planet, summary) in enumerate(_ZODIAC_DATA):
        if month_day < start:
            insight_data = _ZODIAC_DATA[index - 1]
            break
    else:
        # month_day is on or after the final start boundary (Capricorn) and should
        # therefore default to Capricorn from the initial assignment above.
        pass

    _, sign, element, planet, summary = insight_data
    return ZodiacInsight(sign=sign, element=element, ruling_planet=planet, summary=summary)


_CHINESE_ANIMALS = [
    "Rat",
    "Ox",
    "Tiger",
    "Rabbit",
    "Dragon",
    "Snake",
    "Horse",
    "Goat",
    "Monkey",
    "Rooster",
    "Dog",
    "Pig",
]

_CHINESE_TRAITS = {
    "Rat": "strategic, charming, and resourceful when navigating changing tides.",
    "Ox": "patient, steadfast, and devoted to purposeful progress.",
    "Tiger": "courageous, magnetic, and ready to champion the underdog.",
    "Rabbit": "artistic, gentle, and a natural curator of peaceful spaces.",
    "Dragon": "dynamic, visionary, and able to catalyze collective momentum.",
    "Snake": "intuitive, refined, and wise in the art of timing.",
    "Horse": "restless, free-spirited, and happiest chasing open horizons.",
    "Goat": "tender-hearted, imaginative, and committed to cooperative harmony.",
    "Monkey": "clever, playful, and ingenious when solving intricate puzzles.",
    "Rooster": "confident, precise, and devoted to uplifting community standards.",
    "Dog": "loyal, sincere, and moved by a strong moral compass.",
    "Pig": "kind, generous, and gifted at transmuting challenges into abundance.",
}


@dataclass(frozen=True)
class ChineseZodiacInsight:
    animal: str
    element_cycle: str
    summary: str


def chinese_zodiac_for(birthdate: date) -> ChineseZodiacInsight:
    """Return the Chinese zodiac insight for ``birthdate``."""

    cycle_index = (birthdate.year - 1900) % len(_CHINESE_ANIMALS)
    animal = _CHINESE_ANIMALS[cycle_index]
    element_cycle = _five_element_cycle(birthdate.year)
    summary = _CHINESE_TRAITS[animal]
    return ChineseZodiacInsight(animal=animal, element_cycle=element_cycle, summary=summary)


def _five_element_cycle(year: int) -> str:
    elements = [
        "Metal",
        "Metal",
        "Water",
        "Water",
        "Wood",
        "Wood",
        "Fire",
        "Fire",
        "Earth",
        "Earth",
    ]
    index = (year - 1900) % len(elements)
    element = elements[index]
    yin_yang = "Yang" if ((year - 1900) % 2 == 0) else "Yin"
    return f"{yin_yang} {element}"
