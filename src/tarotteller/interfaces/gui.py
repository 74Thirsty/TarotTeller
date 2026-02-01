"""Graphical interface for TarotTeller using Tkinter."""

from __future__ import annotations

import textwrap
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, ttk
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
        self.root.title(BRAND_NAME)
        self.root.configure(bg="#f6f4fb")
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
        self.root.geometry("980x720")
        self.root.minsize(820, 600)

        container = ttk.Frame(self.root, style="App.TFrame", padding=24)
        container.pack(fill=tk.BOTH, expand=True)

        header = ttk.Frame(container, style="App.TFrame")
        header.pack(fill=tk.X)

        header_text = ttk.Frame(header, style="App.TFrame")
        header_text.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(header_text, text=BRAND_NAME, style="Brand.TLabel").pack(
            anchor=tk.W
        )
        ttk.Label(
            header_text,
            text="Insightful, multi-layered tarot readings for modern mystics.",
            style="SubBrand.TLabel",
        ).pack(anchor=tk.W, pady=(4, 0))

        ttk.Label(
            header,
            text=f"v{APP_VERSION}",
            style="Badge.TLabel",
        ).pack(side=tk.RIGHT, padx=(12, 0))

        ttk.Separator(container, orient=tk.HORIZONTAL).pack(
            fill=tk.X, pady=(16, 18)
        )

        controls = ttk.LabelFrame(
            container, text="Reading setup", style="Card.TLabelframe", padding=16
        )
        controls.pack(side=tk.TOP, fill=tk.X, pady=(0, 16))
        controls.columnconfigure(1, weight=1)
        controls.columnconfigure(3, weight=0)
        controls.columnconfigure(4, weight=1)

        # Spread selection
        ttk.Label(controls, text="Spread:", style="Card.TLabel").grid(
            row=0, column=0, sticky=tk.W
        )
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
        ttk.Label(controls, text="Cards:", style="Card.TLabel").grid(
            row=0, column=2, sticky=tk.W
        )
        self.card_entry = ttk.Entry(controls, textvariable=self.card_count, width=6)
        self.card_entry.grid(row=0, column=3, sticky=tk.W, padx=(4, 16))
        ttk.Label(
            controls, text="(leave blank to use spread)", style="Card.TLabel"
        ).grid(row=0, column=4, sticky=tk.W)

        # Question input
        ttk.Label(controls, text="Question:", style="Card.TLabel").grid(
            row=1, column=0, sticky=tk.NW, pady=(12, 0)
        )
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
            highlightcolor="#7b61d1",
            padx=8,
            pady=8,
            background="#ffffff",
            foreground="#2e1f4f",
            insertbackground="#2e1f4f",
        )

        ttk.Label(
            controls,
            text="Tip: Share who or what you're reading for, any timeframe (for example 'next month'), and how you feel so TarotTeller can tailor the insights.",
            style="CardHint.TLabel",
            wraplength=520,
            justify=tk.LEFT,
        ).grid(row=2, column=1, columnspan=4, sticky=tk.W, pady=(4, 0))

        # Seed entry
        ttk.Label(controls, text="Shuffle Seed:", style="Card.TLabel").grid(
            row=3, column=0, sticky=tk.W
        )
        self.seed_var = tk.StringVar(value="")
        self.seed_entry = ttk.Entry(controls, textvariable=self.seed_var, width=10)
        self.seed_entry.grid(row=3, column=1, sticky=tk.W, padx=(4, 16))

        # Options row
        options = ttk.Frame(controls, style="Card.TFrame")
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

        ttk.Label(options, text="Tone:", style="Card.TLabel").pack(
            side=tk.LEFT, padx=(16, 4)
        )
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
            style="CardHint.TLabel",
            wraplength=760,
            justify=tk.LEFT,
        ).grid(row=4, column=0, columnspan=5, sticky=tk.W, pady=(12, 0))

        # Action buttons
        actions = ttk.Frame(container, style="App.TFrame")
        actions.pack(fill=tk.X, pady=(0, 16))
        draw_button = ttk.Button(
            actions, text="Draw Reading", style="Accent.TButton", command=self.draw_reading
        )
        draw_button.pack(side=tk.LEFT)

        reset_button = ttk.Button(
            actions, text="Reset Deck", style="Secondary.TButton", command=self.reset_deck
        )
        reset_button.pack(side=tk.LEFT, padx=(12, 0))

        help_button = ttk.Button(
            actions, text="Help", style="Secondary.TButton", command=self._show_help
        )
        help_button.pack(side=tk.LEFT, padx=(12, 0))

        # Output area
        output_frame = ttk.LabelFrame(
            container, text="Reading output", style="Card.TLabelframe", padding=12
        )
        output_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 16))

        self.output = tk.Text(output_frame, wrap=tk.WORD, font=("TkDefaultFont", 11))
        self.output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.output.configure(
            borderwidth=0,
            highlightthickness=1,
            highlightbackground="#d9d9d9",
            highlightcolor="#7b61d1",
            padx=12,
            pady=12,
            spacing1=4,
            spacing3=6,
            background="#ffffff",
            foreground="#2e1f4f",
            insertbackground="#2e1f4f",
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

        self.root.option_add("*Font", "Segoe UI 10")

        style.configure("TFrame", background="#f6f4fb")
        style.configure("TLabel", background="#f6f4fb", foreground="#2e1f4f")
        style.configure("TSeparator", background="#e4ddf3")
        style.configure("App.TFrame", background="#f6f4fb")
        style.configure(
            "Brand.TLabel",
            font=("Segoe UI", 22, "bold"),
            foreground="#2e1f4f",
        )
        style.configure(
            "SubBrand.TLabel",
            font=("Segoe UI", 11),
            foreground="#5b4b8a",
        )
        style.configure(
            "Hint.TLabel",
            foreground="#4b3c70",
            background="#f6f4fb",
            wraplength=520,
        )
        style.configure("Card.TFrame", background="#ffffff")
        style.configure(
            "Card.TLabel",
            background="#ffffff",
            foreground="#2e1f4f",
        )
        style.configure(
            "CardHint.TLabel",
            foreground="#4b3c70",
            background="#ffffff",
            wraplength=520,
        )
        style.configure(
            "Badge.TLabel",
            background="#ece8f6",
            foreground="#5b4b8a",
            padding=(10, 4),
            font=("Segoe UI", 9, "bold"),
        )
        style.configure(
            "Card.TLabelframe",
            background="#ffffff",
            foreground="#2e1f4f",
            borderwidth=1,
            relief="solid",
        )
        style.configure(
            "Card.TLabelframe.Label",
            background="#ffffff",
            foreground="#2e1f4f",
            font=("Segoe UI", 10, "bold"),
        )
        style.configure(
            "Accent.TButton",
            padding=(14, 8),
            background="#6d4dd2",
            foreground="#ffffff",
            font=("Segoe UI", 10, "bold"),
        )
        style.map(
            "Accent.TButton",
            background=[("active", "#5c3ec2"), ("pressed", "#5c3ec2")],
        )
        style.configure(
            "Secondary.TButton",
            padding=(12, 8),
            background="#e9e2fb",
            foreground="#3a2d5f",
        )
        style.map(
            "Secondary.TButton",
            background=[("active", "#dbd1f6"), ("pressed", "#dbd1f6")],
        )
        style.configure(
            "Status.TLabel",
            font=("Segoe UI", 10),
            background="#ece8f6",
            foreground="#4b3c70",
        )
        style.configure("TCombobox", padding=6)

    def _build_menu(self) -> None:
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar)
        file_menu.add_command(
            label="Export Reading...",
            accelerator="Ctrl+S",
            command=self._export_reading,
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", accelerator="Ctrl+Q", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        reading_menu = tk.Menu(menubar)
        reading_menu.add_command(
            label="Draw Reading",
            accelerator="Ctrl+Enter",
            command=self.draw_reading,
        )
        reading_menu.add_command(
            label="Reset Deck", accelerator="Ctrl+R", command=self.reset_deck
        )
        reading_menu.add_separator()
        reading_menu.add_command(
            label="Clear Output",
            command=self._clear_output,
            accelerator="Ctrl+L",
        )
        menubar.add_cascade(label="Reading", menu=reading_menu)

        edit_menu = tk.Menu(menubar)
        edit_menu.add_command(
            label="Copy Reading",
            accelerator="Ctrl+Shift+C",
            command=self._copy_output,
        )
        edit_menu.add_command(
            label="Copy Question",
            accelerator="Ctrl+Shift+Q",
            command=self._copy_question,
        )
        edit_menu.add_separator()
        edit_menu.add_command(
            label="Clear Question",
            accelerator="Ctrl+Shift+L",
            command=self._clear_question,
        )
        menubar.add_cascade(label="Edit", menu=edit_menu)

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
        self.root.bind_all("<Control-s>", self._trigger_export)
        self.root.bind_all("<Control-S>", self._trigger_export)
        self.root.bind_all("<Control-Shift-C>", self._trigger_copy_output)
        self.root.bind_all("<Control-Shift-Q>", self._trigger_copy_question)
        self.root.bind_all("<Control-Shift-L>", self._trigger_clear_question)

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

    def _export_reading(self) -> None:
        content = self.output.get("1.0", tk.END).strip()
        if not content:
            messagebox.showinfo(
                "Nothing to export", "Draw a reading before exporting."
            )
            self._set_status("Export canceled: no reading available.")
            return

        default_name = f"tarot-reading-{datetime.now().strftime('%Y%m%d-%H%M')}.txt"
        file_path = filedialog.asksaveasfilename(
            title="Export reading",
            defaultextension=".txt",
            initialfile=default_name,
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not file_path:
            self._set_status("Export canceled.")
            return

        try:
            with open(file_path, "w", encoding="utf-8") as handle:
                handle.write(content)
        except OSError as exc:
            messagebox.showerror("Export failed", str(exc))
            self._set_status("Export failed.")
            return

        self._set_status(f"Reading exported to {file_path}.")

    def _copy_output(self) -> None:
        content = self.output.get("1.0", tk.END).strip()
        if not content:
            self._set_status("Nothing to copy from the reading output.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        self._set_status("Reading copied to clipboard.")

    def _copy_question(self) -> None:
        content = self.question.get("1.0", tk.END).strip()
        if not content:
            self._set_status("Nothing to copy from the question field.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        self._set_status("Question copied to clipboard.")

    def _clear_question(self) -> None:
        self.question.delete("1.0", tk.END)
        self._set_status("Question cleared.")

    def _trigger_export(self, event: Optional[tk.Event] = None) -> str:
        self._export_reading()
        return "break"

    def _trigger_copy_output(self, event: Optional[tk.Event] = None) -> str:
        self._copy_output()
        return "break"

    def _trigger_copy_question(self, event: Optional[tk.Event] = None) -> str:
        self._copy_question()
        return "break"

    def _trigger_clear_question(self, event: Optional[tk.Event] = None) -> str:
        self._clear_question()
        return "break"

    def _trigger_help(self, event: Optional[tk.Event] = None) -> str:
        self._show_help()
        return "break"


def launch() -> None:
    """Convenience entry point for running the GUI."""

    app = TarotTellerApp()
    app.run()


__all__ = ["TarotTellerApp", "launch"]
