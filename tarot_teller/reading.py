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


def _intention_focus(intention: str | None, context: str) -> str:
    """Return a sentence that anchors the section back to the user's focus."""

    if not intention:
        return context
    return f"With your focus on {intention}, {context}"


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
        sections = (
            _render_panel(
                "✨ Welcome",
                _greeting_section(
                    user.name,
                    user.favorite_color,
                    self.color_message,
                    user.intention,
                ),
            ),
            _render_panel(
                "🌌 Celestial Alignments",
                _astro_section(
                    self.western_zodiac,
                    self.chinese_zodiac,
                    user.intention,
                ),
            ),
            _render_panel(
                "🪶 Medicine Wheel Guidance",
                _totem_section(self.totem, user.intention),
            ),
            _render_panel(
                "🔢 Chaldean Numerology",
                _numerology_section(self.numerology, user.intention),
            ),
            _render_panel(
                "🃏 Three-Card Tarot Spread",
                _tarot_section(self.tarot, user.intention),
            ),
        )
        summary = _render_panel(
            "🔮 Integrated Summary",
            _synthesis_section(
                self.western_zodiac,
                self.chinese_zodiac,
                self.totem,
                self.numerology,
                self.tarot,
                user,
            ),
        )

        banner = _modern_banner(user.name)

        return "\n\n".join((banner, *sections, summary))


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


def _modern_banner(name: str) -> str:
    """Return a stylised header for the reading."""

    heading = f"TarotTeller Insight for {name}"
    padding = 4
    width = max(len(heading) + padding, 48)
    line = "═" * width
    centered = heading.center(width)
    return "\n".join((line, centered, line))


def _greeting_section(name: str, color: str, color_message: str, intention: str | None) -> str:
    intention_text = (
        f"You asked me to hold the intention of '{intention}'. I kept that focus while weaving this reading."
        if intention
        else "You invited a general reading, so I listened for the themes most alive around you."
    )
    return dedent(
        f"""
        Hello {name}! Tonight I light a {color.lower()} candle in your honor;
        this hue resonates with {color_message}
        and threads its resonance through every insight that follows. {intention_text}
        """
    ).strip()


def _astro_section(
    western: ZodiacInsight,
    chinese: ChineseZodiacInsight,
    intention: str | None,
) -> str:
    focus = _intention_focus(
        intention,
        "let these celestial rhythms highlight timing windows for your next steps.",
    )
    return dedent(
        f"""
        In western astrology you are a {western.sign}, an {western.element.lower()} sign guided by {western.ruling_planet}.
        {western.summary}

        Your Chinese zodiac ally is the {chinese.animal} within the {chinese.element_cycle} year cycle. This energy is {chinese.summary}
        and it nudges you to balance patience with swift intuitive action over the coming weeks—{focus}
        """
    ).strip()


def _totem_section(totem: TotemInsight, intention: str | None) -> str:
    qualities = _join_keywords(totem.keywords)
    focus = _intention_focus(
        intention,
        "invite these qualities into practical rituals or boundaries that protect what matters most to you.",
    )
    return dedent(
        f"""
        The {totem.totem} totem from the {totem.clan} greets you, radiating {qualities} qualities.
        {totem.message} As you move through your days, {focus}
        """
    ).strip()


def _numerology_section(numerology: NumerologyInsight, intention: str | None) -> str:
    breakdown = ", ".join(f"{char}={value}" for char, value in numerology.name_breakdown)
    if not breakdown:
        breakdown = "(no letters mapped—consider providing a different name or nickname)"
    focus = _intention_focus(
        intention,
        "use repeating numbers and serendipities as signposts confirming you're aligned with your aim.",
    )
    return dedent(
        f"""
        Name vibration breakdown: {breakdown}. {numerology.summary}
        Together these frequencies encourage you to notice repeating numbers, serendipities, and subtle invitations this week—{focus}
        """
    ).strip()


def _tarot_section(tarot: TarotReading, intention: str | None) -> str:
    focus = _intention_focus(
        intention,
        "let each card reveal one small action that supports your desired outcome.",
    )
    return dedent(
        f"""
        {tarot.summary()}
        These cards form a narrative arc from what shaped you to what is emerging—feel into where each sentence lands in your body and {focus}
        """
    ).strip()


def _synthesis_section(
    western: ZodiacInsight,
    chinese: ChineseZodiacInsight,
    totem: TotemInsight,
    numerology: NumerologyInsight,
    tarot: TarotReading,
    user: UserProfile,
) -> str:
    anchor = tarot.spread[-1].card.name if tarot.spread else "your evolving story"
    totem_qualities = _join_keywords(totem.keywords)
    intention = user.intention
    if intention:
        intention_line = (
            f"Everything circles back to your focus on {intention}. Choose one meaningful action that honours this aim in the next 72 hours."
        )
    else:
        intention_line = (
            "Follow the thread that feels most alive over the next 72 hours and capture insights in a journal, ritual, or conversation."
        )

    key_takeaways = [
        f"• Celestial: lean into {western.element.lower()} practices while coordinating decisions when {chinese.animal.lower()} energy feels strongest.",
        f"• Totem: call on the {totem.totem.lower()} for {totem_qualities} support whenever self-doubt creeps in.",
        f"• Numerology: numbers {numerology.name_number} and {numerology.birth_number} confirm aligned opportunities.",
        f"• Tarot: the {anchor} card anchors the story and marks the moment you embody the lesson.",
    ]
    takeaway_text = "\n".join(key_takeaways)

    return dedent(
        f"""
        Threads from your {western.sign} sun, {chinese.animal} year, and {totem.totem} medicine weave a tapestry of {totem_qualities} resilience.
        Numerology reminds you that your name and birth promise resonate with numbers {numerology.name_number} and {numerology.birth_number};
        let these guideposts support your decisions while the tarot clarifies the emotional landscape of your choices.

        {takeaway_text}

        As you move forward, imagine the wisdom of {anchor.lower()} illuminating your path. {intention_line}
        Your guides and ancestors are listening.
        """
    ).strip()


def _join_keywords(words: tuple[str, ...]) -> str:
    if not words:
        return ""
    if len(words) == 1:
        return words[0]
    return ", ".join(words[:-1]) + f", and {words[-1]}"


def _render_panel(title: str, body: str) -> str:
    """Render a block with a modern, panel-like appearance."""

    body_lines = [line.rstrip() for line in body.splitlines()]
    content_width = max((len(line) for line in body_lines), default=0)
    width = max(len(title) + 4, content_width + 2)
    horizontal = "─" * width
    header = f"┌{horizontal}┐"
    title_line = f"│ {title.ljust(width - 1)}│"
    separator = f"├{horizontal}┤"
    content = "\n".join(f"│ {line.ljust(width - 1)}│" for line in body_lines)
    footer = f"└{horizontal}┘"
    if not content:
        content = f"│ {'':{width - 1}}│"
    return "\n".join((header, title_line, separator, content, footer))
