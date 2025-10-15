from tarotteller.context import analyze_question
from tarotteller.deck import TarotDeck
from tarotteller.engine import InterpretationEngine
from tarotteller.knowledge import TarotKnowledgeBase
from tarotteller.spreads import draw_spread


def test_render_personalised_summary_creates_story_arc():
    deck = TarotDeck()
    deck.seed(11)
    deck.reset(shuffle=True)
    reading = draw_spread(deck, "three_card", allow_reversed=False, rng=7)
    profile = analyze_question(
        "How can I nurture my career and creativity this month?"
    )

    engine = InterpretationEngine(TarotKnowledgeBase(deck.all_cards))
    summary = engine.render_personalised_summary(reading, profile)

    assert "Story Arc" in summary
    assert "You arrive with a" in summary
    assert "chapter of" in summary
