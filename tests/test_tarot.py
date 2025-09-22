import random

from tarot_teller.tarot import draw_three_card_spread


def test_three_card_spread_is_deterministic_with_seed():
    rng = random.Random(42)
    reading = draw_three_card_spread(rng)
    cards = tuple(entry.card.name for entry in reading.spread)
    assert len(cards) == 3
    assert len(set(cards)) == 3
    assert cards == (
        "Judgement",
        "The Empress",
        "The Fool",
    )
