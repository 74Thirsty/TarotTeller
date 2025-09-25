from tarotteller.deck import TarotDeck


def test_deck_contains_full_set():
    deck = TarotDeck()
    cards = deck.all_cards
    assert len(cards) == 78
    assert sum(1 for card in cards if card.arcana == "major") == 22
    assert sum(1 for card in cards if card.arcana == "minor") == 56
    assert len({card.name for card in cards}) == 78


def test_get_card_case_insensitive():
    deck = TarotDeck()
    card = deck.get_card(" the fool ")
    assert card is not None
    assert card.name == "The Fool"


def test_draw_reduces_stack():
    deck = TarotDeck()
    original_remaining = len(deck)
    drawn = deck.draw(3)
    assert len(drawn) == 3
    assert len(deck) == original_remaining - 3


def test_draw_without_reversals():
    deck = TarotDeck()
    deck.seed(123)
    deck.reset(shuffle=True)
    drawn = deck.draw(5, allow_reversed=False)
    assert all(not card.is_reversed for card in drawn)
