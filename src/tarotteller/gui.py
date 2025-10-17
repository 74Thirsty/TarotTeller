"""Graphical interface for TarotTeller using Tkinter."""

from __future__ import annotations

import textwrap
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Iterable, List, Optional

from .context import analyze_question
from .deck import DrawnCard, TarotDeck
from .engine import InterpretationEngine
from .experiences import build_immersive_companion
from .knowledge import TarotKnowledgeBase
from .spreads import SPREADS, SpreadReading, draw_spread


_TEXT_WRAP_WIDTH = 72


def _wrap_prompt(text: str) -> str:
    wrapper = textwrap.TextWrapper(
        width=_TEXT_WRAP_WIDTH, initial_indent="   ", subsequent_indent="   "
    )
    return wrapper.fill(text)


def _format_simple_reading(reading: SpreadReading) -> str:
    lines: List[str] = []
    for placement in reading.placements:
        card = placement.card
        prompt = _wrap_prompt(placement.position.prompt)
        meaning = textwrap.indent(card.meaning, "   ")
        lines.append(
            f"{placement.position.index}. {card.card.name} ({card.orientation})\n"
            f"{prompt}\n"
            f"{meaning}"
        )
    return "\n\n".join(lines)


def _format_direct_draw(cards: Iterable[DrawnCard]) -> str:
    formatted: List[str] = []
    for index, card in enumerate(cards, start=1):
        meaning = textwrap.indent(card.meaning, "   ")
        formatted.append(
            f"Card {index}: {card.card.name} ({card.orientation})\n{meaning}"
        )
    return "\n\n".join(formatted)


class TarotTellerApp:
    """Tkinter application shell for the TarotTeller GUI."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("TarotTeller")
        self.deck = TarotDeck()
        self._build_layout()

    def _build_layout(self) -> None:
        self.root.geometry("880x640")
        self.root.minsize(720, 520)

        container = ttk.Frame(self.root, padding=16)
        container.pack(fill=tk.BOTH, expand=True)

        controls = ttk.Frame(container)
        controls.pack(side=tk.TOP, fill=tk.X, pady=(0, 12))

        # Spread selection
        ttk.Label(controls, text="Spread:").grid(row=0, column=0, sticky=tk.W)
        self.spread_var = tk.StringVar(value="single")
        spread_choices = sorted(SPREADS.keys())
        self.spread_box = ttk.Combobox(
            controls,
            textvariable=self.spread_var,
            values=spread_choices,
            state="readonly",
            width=18,
        )
        self.spread_box.grid(row=0, column=1, sticky=tk.W, padx=(4, 16))

        # Card count override
        ttk.Label(controls, text="Cards:").grid(row=0, column=2, sticky=tk.W)
        self.card_count = tk.StringVar(value="")
        self.card_entry = ttk.Entry(controls, textvariable=self.card_count, width=6)
        self.card_entry.grid(row=0, column=3, sticky=tk.W, padx=(4, 16))
        ttk.Label(controls, text="(leave blank to use spread)").grid(
            row=0, column=4, sticky=tk.W
        )

        # Question input
        ttk.Label(controls, text="Question:").grid(
            row=1, column=0, sticky=tk.NW, pady=(12, 0)
        )
        self.question = tk.Text(controls, height=3, width=60)
        self.question.grid(row=1, column=1, columnspan=4, sticky=tk.W, pady=(12, 0))

        # Seed entry
        ttk.Label(controls, text="Shuffle Seed:").grid(row=2, column=0, sticky=tk.W)
        self.seed_var = tk.StringVar(value="")
        self.seed_entry = ttk.Entry(controls, textvariable=self.seed_var, width=10)
        self.seed_entry.grid(row=2, column=1, sticky=tk.W, padx=(4, 16))

        # Options row
        options = ttk.Frame(controls)
        options.grid(row=2, column=2, columnspan=3, sticky=tk.W)

        self.allow_reversed = tk.BooleanVar(value=True)
        ttk.Checkbutton(options, text="Allow reversed", variable=self.allow_reversed).pack(
            side=tk.LEFT
        )

        self.detailed = tk.BooleanVar(value=False)
        ttk.Checkbutton(options, text="Detailed spread view", variable=self.detailed).pack(
            side=tk.LEFT, padx=(12, 0)
        )

        self.immersive = tk.BooleanVar(value=False)
        ttk.Checkbutton(options, text="Immersive companion", variable=self.immersive).pack(
            side=tk.LEFT, padx=(12, 0)
        )

        ttk.Label(options, text="Tone:").pack(side=tk.LEFT, padx=(16, 4))
        self.tone = tk.StringVar(value="radiant")
        tone_menu = ttk.Combobox(
            options,
            textvariable=self.tone,
            values=["radiant", "mystic", "grounded"],
            state="readonly",
            width=10,
        )
        tone_menu.pack(side=tk.LEFT)

        # Action buttons
        actions = ttk.Frame(container)
        actions.pack(fill=tk.X)
        draw_button = ttk.Button(actions, text="Draw Reading", command=self.draw_reading)
        draw_button.pack(side=tk.LEFT)

        reset_button = ttk.Button(actions, text="Reset Deck", command=self.reset_deck)
        reset_button.pack(side=tk.LEFT, padx=(12, 0))

        # Output area
        output_frame = ttk.Frame(container)
        output_frame.pack(fill=tk.BOTH, expand=True, pady=(12, 0))

        self.output = tk.Text(output_frame, wrap=tk.WORD, font=("TkDefaultFont", 11))
        self.output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(output_frame, command=self.output.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output.configure(yscrollcommand=scrollbar.set)

    def run(self) -> None:
        self.root.mainloop()

    def reset_deck(self) -> None:
        seed_text = self.seed_var.get().strip()
        try:
            seed_value = int(seed_text) if seed_text else None
        except ValueError:
            messagebox.showerror("Invalid seed", "Seed must be an integer value.")
            return
        self.deck = TarotDeck()
        if seed_value is not None:
            self.deck.seed(seed_value)
        self.deck.reset(shuffle=True)
        messagebox.showinfo("Deck reset", "Deck reshuffled and ready for a new reading.")

    def draw_reading(self) -> None:
        try:
            seed_value = self._parse_optional_int(self.seed_var.get())
        except ValueError:
            messagebox.showerror("Invalid seed", "Seed must be an integer value.")
            return

        try:
            card_count = self._parse_optional_int(self.card_count.get())
        except ValueError:
            messagebox.showerror("Invalid cards", "Cards must be left blank or an integer.")
            return

        deck = TarotDeck()
        if seed_value is not None:
            deck.seed(seed_value)
        deck.reset(shuffle=True)

        question = self.question.get("1.0", tk.END).strip()
        profile = None
        engine: Optional[InterpretationEngine] = None
        if question:
            profile = analyze_question(question)
            engine = InterpretationEngine(TarotKnowledgeBase(deck.all_cards))

        allow_reversed = self.allow_reversed.get()

        try:
            if card_count:
                drawn = deck.draw(card_count, allow_reversed=allow_reversed)
                rendered = _format_direct_draw(drawn)
                insights_text = ""
                if engine and profile:
                    insights = [engine.build_card_insight(card, profile) for card in drawn]
                    insights_text = "\n\n" + engine.render_for_cards(insights, profile)
                immersive_text = ""
                if self.immersive.get():
                    immersive_text = "\n\n" + build_immersive_companion(
                        drawn, tone=self.tone.get(), profile=profile
                    )
                self._render_output(rendered + insights_text + immersive_text)
                return

            spread_key = self.spread_var.get() or "single"
            if spread_key not in SPREADS:
                raise KeyError(spread_key)
            reading = draw_spread(
                deck,
                spread_key,
                allow_reversed=allow_reversed,
            )
        except (ValueError, KeyError) as exc:
            messagebox.showerror("Unable to draw", str(exc))
            return

        rendered = (
            reading.as_text() if self.detailed.get() else _format_simple_reading(reading)
        )
        insights_text = ""
        if engine and profile:
            insights_text = "\n\n" + engine.render_personalised_summary(reading, profile)

        immersive_text = ""
        if self.immersive.get():
            immersive_text = "\n\n" + build_immersive_companion(
                [placement.card for placement in reading.placements],
                tone=self.tone.get(),
                profile=profile,
            )

        self._render_output(rendered + insights_text + immersive_text)

    def _render_output(self, text: str) -> None:
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, text.strip())
        self.output.see("1.0")

    @staticmethod
    def _parse_optional_int(value: str) -> Optional[int]:
        value = value.strip()
        if not value:
            return None
        return int(value)


def launch() -> None:
    """Convenience entry point for running the GUI."""

    app = TarotTellerApp()
    app.run()


__all__ = ["TarotTellerApp", "launch"]
