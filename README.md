# TarotTeller

TarotTeller is a feature-rich tarot reading toolkit.  It bundles a complete deck,
meaningful spreads, and both a graphical desktop experience and friendly command
line utilities for exploring the cards.  The library is equally at home in
scripts thanks to its expressive Python API.

## Features

- Complete 78 card deck with upright and reversed keywords and descriptions.
- Programmatically generated minor arcana ensure consistent language across suits.
- Built-in spreads, including a single card pull, three card story, and Celtic Cross.
- Desktop GUI with spread selection, contextual question analysis, and immersive
  companion copy for journal work.
- Layered card correspondences blending Chaldean numerology, Western astrology,
  Chinese zodiac wisdom, and Native medicine allies for richer storytelling.
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

## Graphical interface

Launch the desktop experience after installation:

```bash
tarotteller-gui
```

The GUI lets you choose a spread or draw a custom number of cards, analyse a
querent question for personalised insights, and optionally generate the
immersive companion script. Use the **Reset Deck** button to reshuffle with an
optional seed for reproducible sessions.

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

## Enhancement roadmap

The current release draws exclusively on the static tarot metadata defined in
`src/tarotteller/data.py`.  To move toward the "stronger readings" vision for
TarotTeller, plan work in the following stages:

### Immediate technical fixes

- Replace any future bespoke astronomy routines with an industrial-grade
  ephemeris source such as NASA/JPL's SPICE data services to ensure accurate
  planetary positions.
- Introduce transfer learning with a pre-trained language model (e.g., BERT or
  GPT) and wrap it with natural language understanding so the app can parse
  nuanced user prompts before generating readings.

### Knowledge and reasoning upgrades

- Design a comprehensive knowledge graph that captures detailed card meanings,
  astrological correspondences, symbolism, and historical patterns.
- Explore graph neural networks (GNNs) to reason over that graph, enabling the
  engine to connect disparate archetypes during an interpretation.

### System architecture improvements

- Structure the platform as a pipeline: context analyzer → knowledge base → ML
  engine → quality assurance → feedback loop.  Ensure each component exposes
  clear interfaces and confidence scores so downstream checks can gate output.

### Implementation highlights

- Upgrade the ML layer with deep neural networks for generating interpretations,
  multimodal learning that links card imagery to meanings, and probabilistic
  models for better nuance.
- Personalize readings by tracking user interaction history, applying
  collaborative filtering, and experimenting with reinforcement learning to
  adapt responses to individual preferences.
- Reinforce quality by instituting multi-stage verification, adding GAN-based
  polish for natural language, and automating accuracy tests across canonical
  readings.

### Metrics to monitor

- Reading quality: user satisfaction, completion rates, return visits, and time
  spent per session.
- System health: coherence scores, accuracy against known interpretations,
  processing time, and error rate reductions over successive releases.
