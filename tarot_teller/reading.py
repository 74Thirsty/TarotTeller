"""Create the full TarotTeller experience."""

from __future__ import annotations

from dataclasses import dataclass
import random
from textwrap import dedent

from .astrology import ChineseZodiacInsight, ZodiacInsight, chinese_zodiac_for, western_zodiac_for
from .native_american import TotemInsight, totem_for
from .numerology import NumerologyInsight, chaldean_numerology_for
from .tarot import TarotReading, draw_three_card_spread
from .user import UserProfile


@dataclass(frozen=True)
class FullReading:
    user: UserProfile
    western_zodiac: ZodiacInsight
    chinese_zodiac: ChineseZodiacInsight
    totem: TotemInsight
    numerology: NumerologyInsight
    tarot: TarotReading
    color_message: str

    def render(self) -> str:
        user = self.user
        greeting = _greeting_section(user.name, user.favorite_color, self.color_message, user.intention)
        astro_section = _astro_section(self.western_zodiac, self.chinese_zodiac)
        totem_section = _totem_section(self.totem)
        numerology_section = _numerology_section(self.numerology)
        tarot_section = _tarot_section(self.tarot)
        synthesis = _synthesis_section(self.western_zodiac, self.chinese_zodiac, self.totem, self.numerology, self.tarot)

        return "\n\n".join(
            (
                greeting,
                astro_section,
                totem_section,
                numerology_section,
                tarot_section,
                synthesis,
            )
        )


def craft_full_reading(user: UserProfile, rng: random.Random | None = None) -> FullReading:
    western = western_zodiac_for(user.birthdate)
    chinese = chinese_zodiac_for(user.birthdate)
    totem = totem_for(user.birthdate)
    numerology = chaldean_numerology_for(user.name, user.birthdate)
    tarot = draw_three_card_spread(rng)
    color_message = _interpret_color(user.favorite_color)

    return FullReading(
        user=user,
        western_zodiac=western,
        chinese_zodiac=chinese,
        totem=totem,
        numerology=numerology,
        tarot=tarot,
        color_message=color_message,
    )


_COLOR_SYMBOLISM = {
    "RED": "bold self-advocacy and the ignition of passion projects.",
    "ORANGE": "sacral creativity, confident networking, and vibrant collaboration.",
    "YELLOW": "solar joy, intellect, and the courage to be seen.",
    "GREEN": "healing growth, heart-led leadership, and prosperity.",
    "BLUE": "truthful communication, emotional soothing, and spiritual listening.",
    "PURPLE": "psychic attunement, nobility of purpose, and intuitive mastery.",
    "PINK": "tender self-compassion, romance, and gentle rejuvenation.",
    "BLACK": "protection, potent boundaries, and the power of mystery.",
    "WHITE": "purification, clarity, and luminous new beginnings.",
    "GOLD": "sovereignty, celebratory success, and generosity of spirit.",
    "SILVER": "moonlit reflection, adaptability, and receptive magic.",
}


def _interpret_color(color: str) -> str:
    key = color.strip().upper()
    if key in _COLOR_SYMBOLISM:
        return _COLOR_SYMBOLISM[key]
    if " " in key:
        for word in key.split():
            if word in _COLOR_SYMBOLISM:
                return _COLOR_SYMBOLISM[word]
    return "a personally significant vibration—trust the feeling it evokes in you."


def _greeting_section(name: str, color: str, color_message: str, intention: str | None) -> str:
    intention_text = (
        f"You asked me to hold the intention of '{intention}'. I kept that focus while weaving this reading."
        if intention
        else "You invited a general reading, so I listened for the themes most alive around you."
    )
    return dedent(
        f"""
        ✨ Welcome, {name}!\n
        Tonight I light a {color.lower()} candle in your honor; this hue resonates with {color_message}
        and threads its resonance through every insight that follows. {intention_text}
        """
    ).strip()


def _astro_section(western: ZodiacInsight, chinese: ChineseZodiacInsight) -> str:
    return dedent(
        f"""
        🌌 Celestial Alignments\n
        In western astrology you are a {western.sign}, an {western.element.lower()} sign guided by {western.ruling_planet}.
        {western.summary}

        Your Chinese zodiac ally is the {chinese.animal} within the {chinese.element_cycle} year cycle. This energy is {chinese.summary}
        and it nudges you to balance patience with swift intuitive action over the coming weeks.
        """
    ).strip()


def _totem_section(totem: TotemInsight) -> str:
    qualities = _join_keywords(totem.keywords)
    return dedent(
        f"""
        🪶 Medicine Wheel Guidance\n
        The {totem.totem} totem from the {totem.clan} greets you, radiating {qualities} qualities.
        {totem.message}
        """
    ).strip()


def _numerology_section(numerology: NumerologyInsight) -> str:
    breakdown = ", ".join(f"{char}={value}" for char, value in numerology.name_breakdown)
    if not breakdown:
        breakdown = "(no letters mapped—consider providing a different name or nickname)"
    return dedent(
        f"""
        🔢 Chaldean Numerology\n
        Name vibration breakdown: {breakdown}. {numerology.summary}
        Together these frequencies encourage you to notice repeating numbers, serendipities, and subtle invitations this week.
        """
    ).strip()


def _tarot_section(tarot: TarotReading) -> str:
    return dedent(
        f"""
        🃏 Three-Card Tarot Spread\n
        {tarot.summary()}
        These cards form a narrative arc from what shaped you to what is emerging—feel into where each sentence lands in your body.
        """
    ).strip()


def _synthesis_section(
    western: ZodiacInsight,
    chinese: ChineseZodiacInsight,
    totem: TotemInsight,
    numerology: NumerologyInsight,
    tarot: TarotReading,
) -> str:
    anchor = tarot.spread[-1].card.name if tarot.spread else "your evolving story"
    totem_qualities = _join_keywords(totem.keywords)
    return dedent(
        f"""
        🔮 Integrated Message\n
        Threads from your {western.sign} sun, {chinese.animal} year, and {totem.totem} medicine weave a tapestry of
        {totem_qualities} resilience. Numerology reminds you that your name and birth promise resonate with
        numbers {numerology.name_number} and {numerology.birth_number}; let these guideposts support your decisions.

        As you move forward, imagine the wisdom of {anchor.lower()} illuminating your path. Journal, meditate, or create a ritual
        around these themes within the next three days to anchor them into everyday life. Your guides and ancestors are listening.
        """
    ).strip()


def _join_keywords(words: tuple[str, ...]) -> str:
    if not words:
        return ""
    if len(words) == 1:
        return words[0]
    return ", ".join(words[:-1]) + f", and {words[-1]}"
