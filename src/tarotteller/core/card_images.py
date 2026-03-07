"""Shared tarot card image resolution helpers."""

from __future__ import annotations

import os
from pathlib import Path


def card_image_id(card_name: str) -> str:
    """Return canonical snake_case image identifier for a card name."""

    normalized = card_name.strip().lower().replace("-", " ")
    return "_".join(part for part in normalized.split() if part)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def shared_image_dir() -> Path | None:
    """Resolve the shared card image directory.

    Order:
    1) TAROTTELLER_CARD_IMAGE_DIR
    2) Android deck image folder in this monorepo
    """

    override = os.getenv("TAROTTELLER_CARD_IMAGE_DIR")
    if override:
        path = Path(override).expanduser().resolve()
        if path.exists():
            return path

    candidate = _repo_root() / "tarot_teller_android" / "app" / "assets" / "deck" / "images"
    if candidate.exists():
        return candidate

    return None


def resolve_card_image(card_name: str) -> Path | None:
    """Resolve the PNG path for ``card_name`` if available."""

    base_dir = shared_image_dir()
    if base_dir is None:
        return None

    image_path = base_dir / f"{card_image_id(card_name)}.png"
    if image_path.exists():
        return image_path

    return None
