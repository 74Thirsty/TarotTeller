# TarotTeller

## Project Overview

TarotTeller is a modern Python toolkit for exploring tarot cards through scripted workflows, a friendly command line interface, and an optional desktop experience. It ships with a complete 78-card deck, positional spreads, contextual storytelling, and immersive journaling prompts so that every reading feels intentional and repeatable.

The project is structured as a Python package with a `src` layout. The core logic is located in the `src/tarotteller/core` directory, the command-line and graphical interfaces are in `src/tarotteller/interfaces`, and the narrative generation is in `src/tarotteller/narrative`. The project uses `setuptools` for building and `pytest` for testing.

## Building and Running

### Installation

1.  Create and activate a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
2.  Install the package in editable mode:
    ```bash
    pip install -e .
    ```

### Running the application

*   **Command-line interface:**
    ```bash
    tarotteller --help
    ```
*   **Graphical user interface:**
    ```bash
    tarotteller-gui
    ```

### Running tests

*   Run the test suite using `pytest`:
    ```bash
    pytest
    ```

## Development Conventions

*   **Code Style:** The code follows the standard PEP 8 style guide.
*   **Testing:** The project uses `pytest` for testing. Tests are located in the `tests` directory and mirror the structure of the `src` directory.
*   **Dependencies:** The project has no external dependencies listed in `pyproject.toml` or `requirements.txt`. The `README.md` file mentions Codex integration for AI-assisted readings, but the library used for this is not specified. It is possible that the dependencies are expected to be installed manually.
*   **Versioning:** The project follows semantic versioning.
