"""Graphical interface for TarotTeller using Tkinter."""

from __future__ import annotations

import textwrap
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Iterable, List, Optional

from importlib.metadata import PackageNotFoundError, version

from ..core.context import analyze_question
from ..core.correspondences import describe_card_correspondences
from ..core.deck import DrawnCard, TarotDeck
from ..core.engine import InterpretationEngine, build_prompt_interpretation
from ..core.knowledge import TarotKnowledgeBase
from ..core.spreads import SPREADS, SpreadReading, draw_spread
from ..narrative.immersive import build_immersive_companion


_TEXT_WRAP_WIDTH = 72

try:
    APP_VERSION = version("tarotteller")
except PackageNotFoundError:
    APP_VERSION = "development build"

BRAND_NAME = "TarotTeller Studio"
COPYRIGHT_NOTICE = "© 2024 TarotTeller. All rights reserved."

HELP_TEXT = """
TarotTeller Help
================

Getting Started
---------------
1. Choose a spread from the drop-down menu. Leave "Cards" blank to use the spread's default count or enter a number to override it.
2. (Optional) Enter your question or intention in the "Question" field so TarotTeller can tailor interpretations.
3. (Optional) Provide a shuffle seed if you want reproducible draws. Leave it blank for a fresh shuffle each time.
4. Toggle options to allow reversed cards, show detailed spread layout, or add an immersive storytelling companion.
5. Pick the tone for immersive guidance from the "Tone" selector.

Settings Glossary
-----------------
* **Cards override** lets you pull a quick custom number of cards without using a spread.
* **Shuffle seed** repeats the same draw sequence—great for study or journaling.
* **Allow reversed** flips cards upside down to surface shadow lessons and integration work.
* **Detailed spread view** prints every positional prompt for note-taking.
* **Immersive companion** unlocks numerology, Western astrology, Chinese zodiac, and Native medicine storytelling in the tone you choose.

Drawing a Reading
-----------------
* Click **Draw Reading** to pull cards for the chosen spread.
* Click **Reset Deck** to reshuffle using the current seed (if any).
* The results panel shows each card with a short interpretation that blends the spread prompt with TarotTeller's knowledge base. When you provide a question, additional personalised insight appears below the reading.
@@ -93,310 +103,499 @@ def _format_simple_reading(


def _format_direct_draw(cards: Iterable[DrawnCard]) -> str:
    formatted: List[str] = []
    for index, card in enumerate(cards, start=1):
        meaning = textwrap.indent(card.meaning, "   ")
        correspondences = textwrap.indent(
            describe_card_correspondences(card), "   "
        )
        segments = "\n\n".join(
            segment
            for segment in (meaning, correspondences)
            if segment
        )
        formatted.append(
            f"Card {index}: {card.card.name} ({card.orientation})\n{segments}"
        )
    return "\n\n".join(formatted)


class TarotTellerApp:
    """Tkinter application shell for the TarotTeller GUI."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("TarotTeller")
        self.root.title(BRAND_NAME)
        self.root.configure(bg="#f9f7fd")
        self.root.option_add("*tearOff", False)

        self.deck = TarotDeck()
        self._help_window: Optional[tk.Toplevel] = None

        self.spread_var = tk.StringVar(value="single")
        self.card_count = tk.StringVar(value="")
        self.seed_var = tk.StringVar(value="")
        self.allow_reversed = tk.BooleanVar(value=True)
        self.detailed = tk.BooleanVar(value=False)
        self.immersive = tk.BooleanVar(value=False)
        self.tone = tk.StringVar(value="radiant")
        self.status_var = tk.StringVar(value="Ready for your next reading.")

        self._configure_style()
        self._build_menu()
        self._build_layout()
        self._set_status("Welcome to TarotTeller Studio.")

    def _build_layout(self) -> None:
        self.root.geometry("880x640")
        self.root.minsize(720, 520)

        style = ttk.Style(self.root)
        style.configure("Hint.TLabel", foreground="#444444")
        self.root.geometry("960x680")
        self.root.minsize(760, 540)

        container = ttk.Frame(self.root, padding=16)
        container = ttk.Frame(self.root, padding=20)
        container.pack(fill=tk.BOTH, expand=True)

        controls = ttk.Frame(container)
        header = ttk.Frame(container)
        header.pack(fill=tk.X, pady=(0, 12))

        ttk.Label(header, text=BRAND_NAME, style="Brand.TLabel").pack(
            anchor=tk.W
        )
        ttk.Label(
            header,
            text="Insightful, multi-layered tarot readings for modern mystics.",
            style="SubBrand.TLabel",
        ).pack(anchor=tk.W, pady=(4, 0))

        ttk.Separator(container, orient=tk.HORIZONTAL).pack(
            fill=tk.X, pady=(0, 16)
        )

        controls = ttk.LabelFrame(container, text="Reading setup", padding=16)
        controls.pack(side=tk.TOP, fill=tk.X, pady=(0, 12))
        controls.columnconfigure(1, weight=1)
        controls.columnconfigure(3, weight=0)
        controls.columnconfigure(4, weight=1)

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
        self.question = tk.Text(
            controls,
            height=3,
            width=60,
            wrap=tk.WORD,
            font=("TkDefaultFont", 11),
        )
        self.question.grid(
            row=1, column=1, columnspan=4, sticky=tk.EW, pady=(12, 0)
        )
        self.question.configure(
            borderwidth=0,
            highlightthickness=1,
            highlightbackground="#d9d9d9",
            highlightcolor="#b39ddb",
            padx=8,
            pady=8,
        )

        ttk.Label(
            controls,
            text="Tip: Share who or what you're reading for, any timeframe (for example 'next month'), and how you feel so TarotTeller can tailor the insights.",
            style="Hint.TLabel",
            wraplength=520,
            justify=tk.LEFT,
        ).grid(row=2, column=1, columnspan=4, sticky=tk.W, pady=(4, 0))

        # Seed entry
        ttk.Label(controls, text="Shuffle Seed:").grid(row=3, column=0, sticky=tk.W)
        self.seed_var = tk.StringVar(value="")
        self.seed_entry = ttk.Entry(controls, textvariable=self.seed_var, width=10)
        self.seed_entry.grid(row=3, column=1, sticky=tk.W, padx=(4, 16))

        # Options row
        options = ttk.Frame(controls)
        options.grid(row=3, column=2, columnspan=3, sticky=tk.W)

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

        ttk.Label(
            controls,
            text=(
                "Settings guide: 'Allow reversed' invites upside-down cards for shadow work. "
                "'Detailed spread view' prints every positional prompt. "
                "'Immersive companion' adds numerology, Western astrology, Chinese zodiac, and Native medicine layers in the voice you pick. "
                "Use 'Shuffle Seed' for repeatable draws and the 'Cards' override when you want a quick custom pull."
            ),
            style="Hint.TLabel",
            wraplength=760,
            justify=tk.LEFT,
        ).grid(row=4, column=0, columnspan=5, sticky=tk.W, pady=(12, 0))

        # Action buttons
        actions = ttk.Frame(container)
        actions.pack(fill=tk.X)
        draw_button = ttk.Button(actions, text="Draw Reading", command=self.draw_reading)
        actions.pack(fill=tk.X, pady=(0, 12))
        draw_button = ttk.Button(
            actions, text="Draw Reading", style="Accent.TButton", command=self.draw_reading
        )
        draw_button.pack(side=tk.LEFT)

        reset_button = ttk.Button(actions, text="Reset Deck", command=self.reset_deck)
        reset_button = ttk.Button(
            actions, text="Reset Deck", style="Accent.TButton", command=self.reset_deck
        )
        reset_button.pack(side=tk.LEFT, padx=(12, 0))

        help_button = ttk.Button(actions, text="Help", command=self._show_help)
        help_button = ttk.Button(
            actions, text="Help", style="Accent.TButton", command=self._show_help
        )
        help_button.pack(side=tk.LEFT, padx=(12, 0))

        # Output area
        output_frame = ttk.Frame(container)
        output_frame.pack(fill=tk.BOTH, expand=True, pady=(12, 0))
        output_frame = ttk.LabelFrame(container, text="Reading output", padding=12)
        output_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 12))

        self.output = tk.Text(output_frame, wrap=tk.WORD, font=("TkDefaultFont", 11))
        self.output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.output.configure(
            borderwidth=0,
            highlightthickness=1,
            highlightbackground="#d9d9d9",
            highlightcolor="#b39ddb",
            padx=12,
            pady=12,
            spacing1=4,
            spacing3=6,
        )

        scrollbar = ttk.Scrollbar(output_frame, command=self.output.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output.configure(yscrollcommand=scrollbar.set)

        status = ttk.Label(
            self.root,
            textvariable=self.status_var,
            style="Status.TLabel",
            anchor=tk.W,
            padding=(16, 6),
        )
        status.pack(fill=tk.X, side=tk.BOTTOM)

    def _configure_style(self) -> None:
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("Brand.TLabel", font=("Segoe UI", 20, "bold"))
        style.configure(
            "SubBrand.TLabel",
            font=("Segoe UI", 11),
            foreground="#5b4b8a",
        )
        style.configure("Hint.TLabel", foreground="#444444", wraplength=520)
        style.configure(
            "Accent.TButton",
            padding=(12, 6),
        )
        style.configure(
            "Status.TLabel",
            font=("Segoe UI", 10),
            background="#f0ecfa",
        )

    def _build_menu(self) -> None:
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar)
        file_menu.add_command(
            label="Draw Reading",
            accelerator="Ctrl+Enter",
            command=self.draw_reading,
        )
        file_menu.add_command(
            label="Reset Deck", accelerator="Ctrl+R", command=self.reset_deck
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Clear Output", command=self._clear_output, accelerator="Ctrl+L"
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", accelerator="Ctrl+Q", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        view_menu = tk.Menu(menubar)
        view_menu.add_checkbutton(
            label="Allow Reversed Cards", variable=self.allow_reversed
        )
        view_menu.add_checkbutton(
            label="Detailed Spread View", variable=self.detailed
        )
        view_menu.add_checkbutton(
            label="Immersive Companion", variable=self.immersive
        )
        tone_menu = tk.Menu(view_menu)
        for tone in ("radiant", "mystic", "grounded"):
            tone_menu.add_radiobutton(
                label=tone.title(), value=tone, variable=self.tone
            )
        view_menu.add_cascade(label="Immersive Tone", menu=tone_menu)
        menubar.add_cascade(label="View", menu=view_menu)

        help_menu = tk.Menu(menubar)
        help_menu.add_command(label="View Help", accelerator="F1", command=self._show_help)
        help_menu.add_command(label="About TarotTeller", command=self._show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

        self.root.bind_all("<Control-Return>", self._trigger_draw)
        self.root.bind_all("<Control-KP_Enter>", self._trigger_draw)
        self.root.bind_all("<Control-r>", self._trigger_reset)
        self.root.bind_all("<Control-R>", self._trigger_reset)
        self.root.bind_all("<Control-q>", lambda event: self.root.quit())
        self.root.bind_all("<Control-Q>", lambda event: self.root.quit())
        self.root.bind_all("<Control-l>", self._trigger_clear)
        self.root.bind_all("<Control-L>", self._trigger_clear)
        self.root.bind_all("<F1>", self._trigger_help)

    def run(self) -> None:
        self.root.mainloop()

    def reset_deck(self) -> None:
        seed_text = self.seed_var.get().strip()
        try:
            seed_value = int(seed_text) if seed_text else None
        except ValueError:
            messagebox.showerror("Invalid seed", "Seed must be an integer value.")
            self._set_status("Deck reset aborted: invalid seed.")
            return
        self.deck = TarotDeck()
        if seed_value is not None:
            self.deck.seed(seed_value)
        self.deck.reset(shuffle=True)
        messagebox.showinfo("Deck reset", "Deck reshuffled and ready for a new reading.")
        self._set_status("Deck reset and reshuffled.")

    def draw_reading(self) -> None:
        try:
            seed_value = self._parse_optional_int(self.seed_var.get())
        except ValueError:
            messagebox.showerror("Invalid seed", "Seed must be an integer value.")
            self._set_status("Reading aborted: invalid seed.")
            return

        try:
            card_count = self._parse_optional_int(self.card_count.get())
        except ValueError:
            messagebox.showerror("Invalid cards", "Cards must be left blank or an integer.")
            self._set_status("Reading aborted: invalid card count.")
            return

        deck = TarotDeck()
        knowledge_base = TarotKnowledgeBase(deck.all_cards)
        if seed_value is not None:
            deck.seed(seed_value)
        deck.reset(shuffle=True)

        question = self.question.get("1.0", tk.END).strip()
        profile = None
        engine: Optional[InterpretationEngine] = None
        if question:
            profile = analyze_question(question)
            engine = InterpretationEngine(knowledge_base)

        allow_reversed = self.allow_reversed.get()

        try:
            if card_count:
                drawn = deck.draw(card_count, allow_reversed=allow_reversed)
                rendered = _format_direct_draw(drawn)
                sections: List[str] = [rendered]
                if engine and profile:
                    insights = [engine.build_card_insight(card, profile) for card in drawn]
                    response = engine.render_question_response(insights, profile)
                    if response:
                        sections.insert(0, response)
                    sections.append(engine.render_for_cards(insights, profile))
                if self.immersive.get():
                    sections.append(
                        build_immersive_companion(
                            drawn, tone=self.tone.get(), profile=profile
                        )
                    )
                self._render_output("\n\n".join(section.strip() for section in sections if section))
                self._set_status("Direct draw ready.")
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
            self._set_status("Reading aborted: unable to draw spread.")
            return

        rendered = (
            reading.as_text()
            if self.detailed.get()
            else _format_simple_reading(reading, knowledge_base)
        )
        sections = [rendered]
        if engine and profile:
            insights = engine.insights_for_reading(reading, profile)
            response = engine.render_question_response(
                insights, profile, spread_title=reading.spread.name
            )
            if response:
                sections.insert(0, response)
            sections.append(
                engine.render_personalised_summary(
                    reading, profile, insights=insights
                )
            )

        if self.immersive.get():
            sections.append(
                build_immersive_companion(
                    [placement.card for placement in reading.placements],
                    tone=self.tone.get(),
                    profile=profile,
                )
            )

        self._render_output("\n\n".join(section.strip() for section in sections if section))
        self._set_status("Reading ready.")

    def _render_output(self, text: str) -> None:
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, text.strip())
        self.output.see("1.0")
        if not text.strip():
            self._set_status("Output cleared.")

    def _show_help(self) -> None:
    def _show_help(self, event: Optional[tk.Event] = None) -> None:
        if self._help_window and self._help_window.winfo_exists():
            self._help_window.lift()
            self._help_window.focus_set()
            self._set_status("Help window focused.")
            return

        window = tk.Toplevel(self.root)
        window.title("TarotTeller Help")
        window.geometry("560x480")
        window.transient(self.root)

        frame = ttk.Frame(window, padding=16)
        frame.pack(fill=tk.BOTH, expand=True)

        text_widget = tk.Text(frame, wrap=tk.WORD, font=("TkDefaultFont", 11))
        text_widget.insert(tk.END, HELP_TEXT.strip())
        text_widget.configure(state=tk.DISABLED)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.configure(yscrollcommand=scrollbar.set)

        window.protocol("WM_DELETE_WINDOW", self._close_help)
        self._help_window = window
        self._set_status("Help window opened.")

    def _close_help(self) -> None:
        if self._help_window and self._help_window.winfo_exists():
            self._help_window.destroy()
        self._help_window = None
        self._set_status("Help window closed.")

    def _show_about(self) -> None:
        message = (
            f"{BRAND_NAME}\n"
            f"Version: {APP_VERSION}\n\n"
            "Crafted for immersive tarot storytelling with numerology, astrology, and cultural correspondences.\n\n"
            f"{COPYRIGHT_NOTICE}"
        )
        messagebox.showinfo("About TarotTeller", message)
        self._set_status("About dialog displayed.")

    @staticmethod
    def _parse_optional_int(value: str) -> Optional[int]:
        value = value.strip()
        if not value:
            return None
        return int(value)

    def _set_status(self, message: str) -> None:
        self.status_var.set(message)

    def _trigger_draw(self, event: Optional[tk.Event] = None) -> str:
        self.draw_reading()
        return "break"

    def _trigger_reset(self, event: Optional[tk.Event] = None) -> str:
        self.reset_deck()
        return "break"

    def _clear_output(self) -> None:
        self._render_output("")

    def _trigger_clear(self, event: Optional[tk.Event] = None) -> str:
        self._clear_output()
        return "break"

    def _trigger_help(self, event: Optional[tk.Event] = None) -> str:
        self._show_help()
        return "break"


def launch() -> None:
    """Convenience entry point for running the GUI."""

    app = TarotTellerApp()
    app.run()


__all__ = ["TarotTellerApp", "launch"]
