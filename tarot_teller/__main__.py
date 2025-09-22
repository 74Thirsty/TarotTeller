"""Command line interface for TarotTeller."""

from __future__ import annotations

import argparse
import random

from .reading import craft_full_reading
from .user import collect_user_profile


def main() -> None:
    parser = argparse.ArgumentParser(description="Receive an immersive TarotTeller reading.")
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional random seed to make the tarot spread deterministic.",
    )
    args = parser.parse_args()

    user = collect_user_profile()
    rng = random.Random(args.seed) if args.seed is not None else None
    reading = craft_full_reading(user, rng=rng)
    print()
    print(reading.render())


if __name__ == "__main__":  # pragma: no cover - script entry point
    main()
