from pathlib import Path

from engine.deck import REQUIRED_FIELDS, load_deck
from engine.reading import ReadingEngine

DECK_PATH = Path(__file__).resolve().parents[1] / "assets" / "deck" / "rider_waite.json"


def test_no_duplicates_in_three_card_draw():
    cards = load_deck(DECK_PATH)
    result = ReadingEngine(cards).draw("three_card", seed="abc123")
    ids = [entry.card.id for entry in result.cards]
    assert len(ids) == len(set(ids)) == 3


def test_seed_determinism_same_seed_same_reading():
    cards = load_deck(DECK_PATH)
    engine = ReadingEngine(cards)
    r1 = engine.draw("celtic_cross", seed="fixed-seed", include_reversals=True)
    r2 = engine.draw("celtic_cross", seed="fixed-seed", include_reversals=True)
    sig1 = [(c.card.id, c.reversed) for c in r1.cards]
    sig2 = [(c.card.id, c.reversed) for c in r2.cards]
    assert sig1 == sig2


def test_reversal_determinism_under_seed():
    cards = load_deck(DECK_PATH)
    engine = ReadingEngine(cards)
    r1 = engine.draw("three_card", seed="reverse-check", include_reversals=True)
    r2 = engine.draw("three_card", seed="reverse-check", include_reversals=True)
    assert [c.reversed for c in r1.cards] == [c.reversed for c in r2.cards]


def test_deck_json_has_required_fields():
    raw = load_deck(DECK_PATH)
    assert len(raw) == 78
    first = raw[0].__dict__.keys()
    assert REQUIRED_FIELDS.issubset(first)
