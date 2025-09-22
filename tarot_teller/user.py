"""Utilities for collecting and representing TarotTeller user data."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class UserProfile:
    """Container describing the person receiving the reading."""

    name: str
    birthdate: date
    favorite_color: str
    intention: str | None = None


def _prompt(prompt: str) -> str:
    """Wrapper around :func:`input` to make testing easier."""

    return input(prompt)


def collect_user_profile() -> UserProfile:
    """Interactively collect details for a new :class:`UserProfile`."""

    name = _prompt("What name should I use for your reading? ").strip()
    while not name:
        print("I want this to feel personal—please share at least a first name.")
        name = _prompt("What name should I use for your reading? ").strip()

    birthdate = _prompt_for_birthdate()

    favorite_color = _prompt("What color resonates with you today? ").strip()
    while not favorite_color:
        print("Every hue carries symbolism. Choose the color calling to you right now.")
        favorite_color = _prompt("What color resonates with you today? ").strip()

    intention = _prompt(
        "Do you have a question, goal, or intention you'd like this reading to explore?\n"
        "(Press enter to skip if you'd prefer a general reading.)\n> "
    ).strip()

    return UserProfile(
        name=name,
        birthdate=birthdate,
        favorite_color=favorite_color,
        intention=intention or None,
    )


def _prompt_for_birthdate() -> date:
    """Ask for and validate a birthdate."""

    help_text = (
        "Please share your date of birth using the ISO format YYYY-MM-DD."
        " This helps me calculate astrological influences accurately."
    )

    while True:
        raw = _prompt("When were you born? (YYYY-MM-DD) ").strip()
        try:
            parsed = datetime.strptime(raw, "%Y-%m-%d").date()
        except ValueError:
            print("I wasn't able to understand that date.")
            print(help_text)
            continue

        if parsed > date.today():
            print("I sense a future birthdate—please provide the actual date you arrived.")
            continue

        return parsed
