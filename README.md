# TarotTeller

TarotTeller is an immersive Python command-line companion that blends five divination traditions into a single, story-rich reading:

1. Western horoscope insights
2. Chinese zodiac wisdom
3. Native American medicine wheel guidance
4. Chaldean numerology vibrations
5. A three-card tarot spread

The experience is intentionally interactive. TarotTeller asks for your name, birthdate, favourite colour, and an optional intention so it can tailor every paragraph of the reading to you.

## Getting started

TarotTeller relies only on Python's standard library. To explore the reading:

```bash
python -m tarot_teller
```

You can optionally make the tarot spread reproducible by passing a seed value:

```bash
python -m tarot_teller --seed 42
```

## Running the tests

A lightweight pytest suite verifies zodiac boundaries, numerology reductions, tarot spreads, and overall reading composition.

```bash
python -m pytest
```

## Project structure

```
tarot_teller/
├── __init__.py                # Package exports
├── __main__.py                # CLI entry point
├── astrology.py               # Western + Chinese zodiac logic
├── native_american.py         # Medicine wheel totem insights
├── numerology.py              # Chaldean numerology helpers
├── reading.py                 # Orchestrates the full reading
├── tarot.py                   # Tarot deck + spread utilities
└── user.py                    # Interactive prompts and profile model
```

The `tests/` directory contains unit tests to keep future enhancements grounded.

## Extending TarotTeller

TarotTeller was designed with modularity in mind. Each tradition lives in its own module, making it straightforward to:

- swap in alternative data sets (e.g., add more tarot spreads or numerology interpretations),
- build a GUI around `craft_full_reading`, or
- integrate additional cultural wisdom traditions.

Pull requests and mystical ideas are always welcome. ✨
