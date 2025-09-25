# TarotTeller

TarotTeller is a feature-rich tarot reading toolkit.  It bundles a complete deck,
meaningful spreads, and a friendly command line interface for exploring the
cards.  The library is equally at home in scripts thanks to its expressive Python
API.

## Features

- Complete 78 card deck with upright and reversed keywords and descriptions.
- Programmatically generated minor arcana ensure consistent language across suits.
- Built-in spreads, including a single card pull, three card story, and Celtic Cross.
- Command line tools for listing cards, viewing rich card profiles, and drawing
  readings with optional deterministic seeding.
- Well-documented Python API suited for automation or experimentation.

## Installation

The project uses a modern `pyproject.toml` configuration.  Install it in editable
mode to try it locally:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Command line usage

```
usage: tarotteller [-h] {list,info,draw} ...
```

Examples:

- List the first few major arcana cards:

  ```bash
  tarotteller list --arcana major --limit 5
  ```

- Draw a quick three card reading without reversals:

  ```bash
  tarotteller draw --spread three_card --no-reversed
  ```

- Pull two cards with deterministic order and orientation:

  ```bash
  tarotteller draw --cards 2 --seed 7 --orientation-seed 11
  ```

## Programmatic usage

Use the Python API for more control over spreads and cards:

```python
from tarotteller import TarotDeck, draw_spread

deck = TarotDeck()
deck.seed(42)
deck.reset(shuffle=True)
reading = draw_spread(deck, "three_card", rng=99)

for placement in reading.placements:
    print(placement.position.title, placement.card.card.name, placement.card.orientation)
```

## Development

Run the automated tests with `pytest`:

```bash
pytest
```
