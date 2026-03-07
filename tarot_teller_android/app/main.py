from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from kivy.core.clipboard import Clipboard
from kivy.lang import Builder
from kivy.properties import BooleanProperty, ListProperty, NumericProperty, ObjectProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp

from engine.deck import DeckCache
from engine.reading import ReadingEngine
from engine.storage import LocalStorage


class HomeScreen(Screen):
    pass


class SpreadScreen(Screen):
    spread = StringProperty("daily")


class ResultScreen(Screen):
    result_cards = ListProperty([])
    result_text = StringProperty("")
    current_card_index = NumericProperty(0)
    current_card_title = StringProperty("Draw a reading to view cards.")
    current_card_orientation = StringProperty("")
    current_card_message = StringProperty("")
    current_card_image = StringProperty("")

    def set_cards(self, cards: list[dict[str, str]]):
        self.result_cards = cards
        self.current_card_index = 0
        self._refresh_current_card()

    def show_previous_card(self):
        if not self.result_cards:
            return
        self.current_card_index = (self.current_card_index - 1) % len(self.result_cards)
        self._refresh_current_card()

    def show_next_card(self):
        if not self.result_cards:
            return
        self.current_card_index = (self.current_card_index + 1) % len(self.result_cards)
        self._refresh_current_card()

    def _refresh_current_card(self):
        if not self.result_cards:
            self.current_card_title = "Draw a reading to view cards."
            self.current_card_orientation = ""
            self.current_card_message = ""
            self.current_card_image = ""
            return

        card = self.result_cards[self.current_card_index]
        self.current_card_title = card["title"]
        self.current_card_orientation = card["orientation"]
        self.current_card_message = card["message"]
        self.current_card_image = card["image"]


class HistoryScreen(Screen):
    history_items = ListProperty([])


class SettingsScreen(Screen):
    reversals_default = BooleanProperty(True)


class RootManager(ScreenManager):
    pass


class TarotTellerApp(MDApp):
    current_result = ObjectProperty(None)

    def build(self):
        self.theme_cls.primary_palette = "DeepPurple"
        self.storage = LocalStorage(Path(self.user_data_dir))
        self.settings = self.storage.load_settings()
        self.deck = DeckCache.get(Path(__file__).parent / "assets" / "deck" / "rider_waite.json")
        self.engine = ReadingEngine(self.deck)
        return Builder.load_file(str(Path(__file__).parent / "ui" / "screens.kv"))

    def new_reading(self, spread: str):
        self.root.get_screen("spread").spread = spread
        self.root.current = "spread"

    def run_reading(self, spread: str, question: str, include_reversals: bool, seed_text: str):
        seed = seed_text.strip() or None
        result = self.engine.draw(
            spread,
            include_reversals=include_reversals,
            question=question,
            seed=seed,
        )
        self.current_result = result

        lines = []
        card_rows = []
        for entry in result.cards:
            orientation = "Reversed" if entry.reversed else "Upright"
            short = (
                entry.card.meaning_reversed_short if entry.reversed else entry.card.meaning_upright_short
            )
            long_text = (
                entry.card.meaning_reversed_long if entry.reversed else entry.card.meaning_upright_long
            )
            lines.append(f"{entry.position}: {entry.card.name} ({orientation})\n{short}\n{long_text}")
            card_rows.append(
                {
                    "title": f"{entry.position}: {entry.card.name}",
                    "orientation": orientation,
                    "message": f"{short}\n\n{long_text}",
                    "image": self._card_image_path(entry.card.id),
                }
            )

        result_screen = self.root.get_screen("result")
        result_screen.set_cards(card_rows)
        result_screen.result_text = "\n\n".join(lines)
        self.root.current = "result"

    def show_previous_card(self):
        self.root.get_screen("result").show_previous_card()

    def show_next_card(self):
        self.root.get_screen("result").show_next_card()

    def _card_image_path(self, card_id: str) -> str:
        image_path = Path(__file__).parent / "assets" / "deck" / "images" / f"{card_id}.png"
        return str(image_path) if image_path.exists() else ""

    def share_current_text(self) -> str:
        text = self.root.get_screen("result").result_text.strip()
        if text:
            Clipboard.copy(text)
        return text

    def save_current_to_history(self):
        if not self.current_result:
            return
        self.storage.append_history(
            {
                "saved_at": datetime.now(timezone.utc).isoformat(),
                "spread": self.current_result.spread,
                "seed": self.current_result.seed,
                "question": self.current_result.question,
                "cards": [
                    {
                        "position": item.position,
                        "id": item.card.id,
                        "name": item.card.name,
                        "reversed": item.reversed,
                    }
                    for item in self.current_result.cards
                ],
            }
        )

    def load_history_screen(self, query: str = ""):
        self.root.get_screen("history").history_items = self.storage.search_history(query)
        self.root.current = "history"

    def save_settings(self, reversals_default: bool):
        self.settings["reversals_default"] = reversals_default
        self.storage.save_settings(self.settings)


if __name__ == "__main__":
    TarotTellerApp().run()
