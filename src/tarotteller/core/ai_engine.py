"""AI integration utilities for TarotTeller readings."""

from __future__ import annotations

import json
import logging
from collections.abc import Callable, Sequence
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, List, Mapping
import re

_LOG_PATH = Path("tarotteller-ai.log")


def _sanitize_text(text: str, *, max_length: int = 800) -> str:
    """Return ``text`` stripped of control characters and HTML brackets."""

    collapsed = re.sub(r"\s+", " ", text).strip()
    collapsed = re.sub(r"[<>`]+", "", collapsed)
    if len(collapsed) > max_length:
        return collapsed[: max_length - 3].rstrip() + "..."
    return collapsed


def _ensure_log_path(path: Path) -> None:
    if path.parent and not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)


class AIEngine:
    """Interface wrapper for Codex / LLM powered tarot interpretations."""

    def __init__(
        self,
        model: str = "gpt-5",
        temperature: float = 0.7,
        *,
        client: Callable[..., Any] | None = None,
        log_path: Path | None = None,
    ) -> None:
        self.model = model
        self.temperature = float(temperature)
        self._client = client
        self._logger = logging.getLogger(__name__)
        self._log_path = log_path or _LOG_PATH

    def generate_reading(
        self,
        question: str,
        spread: Mapping[str, Any] | Sequence[Mapping[str, Any]],
    ) -> Dict[str, Any]:
        """Generate a tarot reading using an external language model."""

        if not question:
            raise ValueError("question must be provided for AI-assisted readings")
        sanitized_question = _sanitize_text(question)

        if isinstance(spread, Mapping):
            placements: Sequence[Mapping[str, Any]] = spread.get("placements", [])  # type: ignore[assignment]
        else:
            placements = spread
        if not placements:
            raise ValueError("spread data must include at least one placement")

        prompt = self._compose_prompt(sanitized_question, placements, spread)
        response = self._call_model(prompt)
        parsed = self._parse_response(response)
        self._audit_record(sanitized_question, placements, parsed)
        return parsed

    # ------------------------------------------------------------------
    # Internal helpers
    def _compose_prompt(
        self,
        question: str,
        placements: Sequence[Mapping[str, Any]],
        spread_payload: Mapping[str, Any] | Sequence[Mapping[str, Any]],
    ) -> str:
        spread_title = "Custom Spread"
        spread_description = ""
        if isinstance(spread_payload, Mapping):
            spread_info = spread_payload.get("spread", {})
            if isinstance(spread_info, Mapping):
                spread_title = str(spread_info.get("name", spread_title))
                spread_description = str(spread_info.get("description", ""))

        lines: List[str] = []
        lines.append(
            "You are Tarot Teller, an expert tarot reader who writes grounded,"
            " compassionate interpretations that align with the supplied deck metadata."
        )
        lines.append(
            "Generate a narrative that weaves the querent's question with the cards"
            " drawn in the spread."
        )
        lines.append("")
        lines.append(f"Question: {question}")
        lines.append(f"Spread: {spread_title} - {spread_description}".strip())
        lines.append("Cards and positions:")
        for placement in placements:
            card_name = str(placement.get("card_name") or placement.get("card") or "Unknown Card")
            position = str(placement.get("position") or placement.get("title") or "Position")
            orientation = str(placement.get("orientation") or "upright")
            prompt = _sanitize_text(str(placement.get("prompt", "")))
            keywords = placement.get("keywords")
            if isinstance(keywords, Sequence) and not isinstance(keywords, (str, bytes)):
                keyword_text = ", ".join(str(keyword) for keyword in keywords)
            else:
                keyword_text = str(keywords or "")
            lines.append(
                f"- {position}: {card_name} ({orientation}) | prompt: {prompt}"
                f" | keywords: {keyword_text}"
            )
        lines.append("")
        lines.append(
            "Respond strictly in JSON with the shape: "
            "{""summary"": str, ""tone"": str, ""card_insights"": "
            "[{""card"": str, ""position"": str, ""message"": str, ""orientation"": str}]}"
        )
        lines.append(
            "Keep the tone consistent with the deck descriptions."
            " Each card insight must focus on actionable guidance."
        )
        return "\n".join(lines)

    def _call_model(self, prompt: str) -> Any:
        if self._client is not None:
            return self._client(prompt=prompt, model=self.model, temperature=self.temperature)

        try:
            from openai import OpenAI  # type: ignore
        except ImportError as exc:  # pragma: no cover - optional dependency
            raise RuntimeError(
                "No AI client provided and the OpenAI SDK is unavailable."
            ) from exc

        client = OpenAI()  # pragma: no cover - network call in production only
        response = client.responses.create(  # pragma: no cover - external service
            model=self.model,
            input=prompt,
            temperature=self.temperature,
            response_format={"type": "json_object"},
        )
        if not getattr(response, "output", None):  # pragma: no cover - defensive
            raise RuntimeError("AI service returned an empty response")
        first_output = response.output[0]
        if not getattr(first_output, "content", None):  # pragma: no cover - defensive
            raise RuntimeError("AI service response did not include content")
        return first_output.content[0].text

    def _parse_response(self, response: Any) -> Dict[str, Any]:
        if isinstance(response, Mapping) and "choices" in response:
            # Legacy ChatCompletion style payload
            choices = response.get("choices", [])
            if not choices:
                raise ValueError("Model response contained no choices")
            message = choices[0].get("message", {})
            content = message.get("content", "")
        elif isinstance(response, Mapping) and "output" in response:
            output = response.get("output", [])
            if not output:
                raise ValueError("Model response contained no output content")
            content_blocks = output[0].get("content", [])
            if not content_blocks:
                raise ValueError("Model response contained no textual content")
            content = content_blocks[0].get("text", "")
        else:
            content = str(response)

        try:
            payload = json.loads(content)
        except json.JSONDecodeError as exc:
            raise ValueError("Model response was not valid JSON") from exc

        summary = str(payload.get("summary", "")).strip()
        tone = str(payload.get("tone", "balanced")).strip() or "balanced"
        card_insights = payload.get("card_insights", [])
        if not summary:
            raise ValueError("Model response missing 'summary'")
        if not isinstance(card_insights, list) or not card_insights:
            raise ValueError("Model response missing 'card_insights'")

        normalized: List[Dict[str, Any]] = []
        for index, entry in enumerate(card_insights, start=1):
            if not isinstance(entry, Mapping):
                raise ValueError("Each card insight must be an object")
            card = str(entry.get("card") or entry.get("card_name") or "").strip()
            message = str(entry.get("message") or entry.get("insight") or "").strip()
            position = str(entry.get("position") or entry.get("title") or f"Card {index}")
            orientation = str(entry.get("orientation") or "upright").strip()
            if not card:
                raise ValueError("Card insight missing card name")
            if not message:
                raise ValueError("Card insight missing message")
            insight_payload = {
                "card": card,
                "message": message,
                "position": position,
                "orientation": orientation,
            }
            if "focus" in entry:
                insight_payload["focus"] = entry["focus"]
            normalized.append(insight_payload)

        result: Dict[str, Any] = {
            "summary": summary,
            "tone": tone,
            "card_insights": normalized,
            "model": self.model,
        }
        if "response_id" in payload:
            result["response_id"] = payload["response_id"]
        if "metadata" in payload:
            result["metadata"] = payload["metadata"]
        return result

    def _audit_record(
        self,
        question: str,
        placements: Sequence[Mapping[str, Any]],
        parsed: Mapping[str, Any],
    ) -> None:
        question_hash = sha256(question.encode("utf-8")).hexdigest()[:16]
        card_list = ";".join(
            f"{placement.get('card_name') or placement.get('card')}|"
            f"{placement.get('orientation', 'upright')}"
            for placement in placements
        )
        response_id = parsed.get("response_id", "local")
        timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
        record = f"{timestamp},{self.model},{question_hash},{card_list},{response_id}\n"
        try:
            _ensure_log_path(self._log_path)
            with self._log_path.open("a", encoding="utf-8") as handle:
                handle.write(record)
        except OSError:  # pragma: no cover - logging failures should not crash
            self._logger.exception("Failed to write AI audit log entry")


__all__ = ["AIEngine"]
