"""Deterministic RNG helpers."""

from __future__ import annotations

import random
from datetime import datetime, timezone


def daily_seed(now: datetime | None = None) -> str:
    """Return YYYY-MM-DD for deterministic daily draws."""

    ref = now or datetime.now(timezone.utc)
    return ref.strftime("%Y-%m-%d")


def build_rng(seed: str | int | None) -> random.Random:
    """Build a seeded RNG, accepting None for non-deterministic fallback."""

    return random.Random(seed)
