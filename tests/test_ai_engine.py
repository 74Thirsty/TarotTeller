"""Tests covering the AI engine integration layer."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tarotteller.core import (
    AIEngine,
    AIReading,
    InterpretationEngine,
    TarotDeck,
    TarotKnowledgeBase,
    analyze_question,
    draw_spread,
)


class DummyClient:
    def __init__(self, payload: dict):
        self._payload = payload
        self.prompt = None
        self.model = None
        self.temperature = None

    def __call__(self, *, prompt: str, model: str, temperature: float):
        self.prompt = prompt
        self.model = model
        self.temperature = temperature
        return json.dumps(self._payload)


@pytest.fixture
def spread_payload() -> dict:
    return {
        "spread": {"name": "Three Card", "description": "Past, present, future."},
        "placements": [
            {
                "index": 1,
                "position": "Past",
                "prompt": "What history is influencing the situation?",
                "card_name": "The Fool",
                "orientation": "upright",
                "keywords": ["beginnings", "optimism"],
            },
            {
                "index": 2,
                "position": "Present",
                "prompt": "Where does the situation currently stand?",
                "card_name": "The Magician",
                "orientation": "reversed",
                "keywords": ["focus"],
            },
        ],
    }


def test_generate_reading_parses_payload_and_logs(tmp_path: Path, spread_payload: dict) -> None:
    response = {
        "summary": "A moment of transition asks for mindful choices.",
        "tone": "mystic",
        "card_insights": [
            {
                "card": "The Fool",
                "position": "Past",
                "message": "Honour the courage that began this journey.",
                "orientation": "upright",
            },
            {
                "card": "The Magician",
                "position": "Present",
                "message": "Channel your will with integrity before acting.",
                "orientation": "reversed",
            },
        ],
        "response_id": "abc123",
    }
    client = DummyClient(response)
    log_path = tmp_path / "ai.log"
    engine = AIEngine(model="gpt-test", temperature=0.2, client=client, log_path=log_path)

    result = engine.generate_reading("<script>How do I stay focused?</script>", spread_payload)

    assert result["summary"] == response["summary"]
    assert result["tone"] == "mystic"
    assert len(result["card_insights"]) == 2
    assert client.model == "gpt-test"
    assert client.temperature == 0.2
    assert "<" not in client.prompt
    assert log_path.exists()
    log_contents = log_path.read_text(encoding="utf-8")
    assert "gpt-test" in log_contents
    assert "abc123" in log_contents


def test_generate_reading_validates_response(spread_payload: dict) -> None:
    client = DummyClient({"summary": "", "card_insights": []})
    engine = AIEngine(client=client)

    with pytest.raises(ValueError):
        engine.generate_reading("What next?", spread_payload)


def test_interpretation_engine_generate_ai_reading(tmp_path: Path) -> None:
    deck = TarotDeck()
    deck.seed(7)
    deck.reset(shuffle=True)
    reading = draw_spread(deck, "three_card", rng=13)
    profile = analyze_question("How do I nurture my creative work this season?")
    insights = [
        {
            "card": placement.card.card.name,
            "position": placement.position.title,
            "message": f"Insight for {placement.position.title}",
            "orientation": placement.card.orientation,
        }
        for placement in reading.placements
    ]
    payload = {
        "summary": "Creativity blossoms when you trust your pacing.",
        "tone": "radiant",
        "card_insights": insights,
        "response_id": "test-response",
    }
    client = DummyClient(payload)
    ai_engine = AIEngine(client=client, log_path=tmp_path / "ai.log")
    knowledge = TarotKnowledgeBase(deck.all_cards)
    engine = InterpretationEngine(knowledge)

    ai_reading = engine.generate_ai_reading(reading, profile, ai_engine=ai_engine, question=profile.question)

    assert isinstance(ai_reading, AIReading)
    assert ai_reading.summary == payload["summary"]
    assert engine.last_ai_reading is ai_reading
    rendered = engine.render_ai_reading(ai_reading, profile)
    assert "AI-Assisted Reading" in rendered
    assert "Creativity blossoms" in rendered
