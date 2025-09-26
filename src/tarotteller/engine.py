"""Interpretation engine that ties spreads to contextual insights."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence

from .context import ContextProfile
from .knowledge import TarotKnowledgeBase
from .spreads import SpreadPlacement, SpreadReading


@dataclass
class PersonalizedInsight:
    """A contextual message generated for a drawn card."""

    placement_index: int
    title: str
    card_name: str
    orientation: str
    prompt: str
    message: str


class InterpretationEngine:
    """Produce contextual readings that blend spreads with question intent."""

    def __init__(self, knowledge_base: TarotKnowledgeBase):
        self._knowledge_base = knowledge_base

    def _select_focus(self, card_themes: Sequence[str], focuses: Sequence[str]) -> str:
        for focus in focuses:
            if focus in card_themes:
                return focus
        if card_themes:
            return card_themes[0]
        return focuses[0] if focuses else "general"

    def _build_insight(
        self,
        placement: SpreadPlacement,
        profile: ContextProfile,
    ) -> PersonalizedInsight:
        card = placement.card
        themes = self._knowledge_base.themes_for_card(card.card)
        focus = self._select_focus(themes, profile.focuses)
        message = self._knowledge_base.insight_for(card, focus)
        return PersonalizedInsight(
            placement_index=placement.position.index,
            title=placement.position.title,
            card_name=card.card.name,
            orientation=card.orientation,
            prompt=placement.position.prompt,
            message=message,
        )

    def insights_for_reading(
        self, reading: SpreadReading, profile: ContextProfile
    ) -> List[PersonalizedInsight]:
        return [self._build_insight(placement, profile) for placement in reading.placements]

    def render_personalised_summary(
        self, reading: SpreadReading, profile: ContextProfile
    ) -> str:
        """Return a multi-line personalised summary for ``reading``."""

        insights = self.insights_for_reading(reading, profile)
        lines: List[str] = []
        lines.append("Personalized Insight")
        lines.append("-------------------")
        lines.append(f"Question : {profile.question}")
        if profile.focuses:
            lines.append(f"Focus    : {', '.join(profile.focuses)}")
        lines.append(f"Timeframe: {profile.timeframe.replace('_', ' ')}")
        lines.append(f"Mood     : {profile.sentiment}")
        if profile.highlighted_terms:
            lines.append(
                "Signals  : " + ", ".join(sorted(profile.highlighted_terms)[:6])
            )
        lines.append("")
        for insight in insights:
            header = (
                f"{insight.placement_index}. {insight.title} — "
                f"{insight.card_name} ({insight.orientation})"
            )
            lines.append(header)
            lines.append("   " + insight.prompt)
            lines.append("   " + insight.message)
            lines.append("")
        lines.append(
            "Let these highlights guide follow-up actions and keep logging feedback to "
            "train the model on what resonates."
        )
        return "\n".join(lines).strip()

    def render_for_cards(
        self, cards: Iterable[PersonalizedInsight], profile: ContextProfile
    ) -> str:
        lines: List[str] = []
        lines.append("Personalized Insight")
        lines.append("-------------------")
        lines.append(f"Question : {profile.question}")
        if profile.focuses:
            lines.append(f"Focus    : {', '.join(profile.focuses)}")
        lines.append(f"Timeframe: {profile.timeframe.replace('_', ' ')}")
        lines.append(f"Mood     : {profile.sentiment}")
        lines.append("")
        for insight in cards:
            header = f"{insight.card_name} ({insight.orientation})"
            lines.append(header)
            lines.append("   " + insight.message)
            lines.append("")
        return "\n".join(lines).strip()

    def build_card_insight(self, drawn_card, profile: ContextProfile) -> PersonalizedInsight:
        themes = self._knowledge_base.themes_for_card(drawn_card.card)
        focus = self._select_focus(themes, profile.focuses)
        message = self._knowledge_base.insight_for(drawn_card, focus)
        return PersonalizedInsight(
            placement_index=0,
            title="",  # Not used for direct draws
            card_name=drawn_card.card.name,
            orientation=drawn_card.orientation,
            prompt="",
            message=message,
        )
