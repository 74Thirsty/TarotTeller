"""Local JSON storage for reading history and settings."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class LocalStorage:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.history_path = self.base_dir / "history.json"
        self.settings_path = self.base_dir / "settings.json"

    def load_history(self) -> list[dict[str, Any]]:
        if not self.history_path.exists():
            return []
        return json.loads(self.history_path.read_text(encoding="utf-8"))

    def save_history(self, records: list[dict[str, Any]]) -> None:
        self.history_path.write_text(json.dumps(records, indent=2), encoding="utf-8")

    def append_history(self, record: dict[str, Any]) -> None:
        history = self.load_history()
        history.insert(0, record)
        self.save_history(history)

    def search_history(self, query: str) -> list[dict[str, Any]]:
        needle = query.lower().strip()
        if not needle:
            return self.load_history()
        return [
            item
            for item in self.load_history()
            if needle in json.dumps(item, ensure_ascii=False).lower()
        ]

    def load_settings(self) -> dict[str, Any]:
        if not self.settings_path.exists():
            return {"theme": "System", "reversals_default": True}
        return json.loads(self.settings_path.read_text(encoding="utf-8"))

    def save_settings(self, settings: dict[str, Any]) -> None:
        self.settings_path.write_text(json.dumps(settings, indent=2), encoding="utf-8")
