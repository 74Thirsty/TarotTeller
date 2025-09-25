from datetime import date
import random

from tarot_teller.reading import craft_full_reading
from tarot_teller.user import UserProfile


def test_full_reading_contains_sections():
    user = UserProfile(
        name="Test Seeker",
        birthdate=date(1990, 7, 5),
        favorite_color="blue",
        intention="clarity about career",
    )
    reading = craft_full_reading(user, rng=random.Random(123))
    rendered = reading.render()

    assert "Celestial Alignments" in rendered
    assert "Medicine Wheel Guidance" in rendered
    assert "Chaldean Numerology" in rendered
    assert "Three-Card Tarot Spread" in rendered
    assert "Integrated Summary" in rendered
    assert "TarotTeller Insight for" in rendered
    assert user.name in rendered
