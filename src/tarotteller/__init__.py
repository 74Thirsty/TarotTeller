"""TarotTeller package exposing tarot deck utilities."""

from .deck import DrawnCard, TarotCard, TarotDeck
from .spreads import SPREADS, draw_spread

__all__ = [
    "DrawnCard",
    "TarotCard",
    "TarotDeck",
    "SPREADS",
    "draw_spread",
]

__version__ = "0.1.0"
