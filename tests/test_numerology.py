from datetime import date

from tarot_teller.numerology import chaldean_numerology_for


def test_numerology_reduction_and_breakdown():
    insight = chaldean_numerology_for("Ada Lovelace", date(1815, 12, 10))
    assert insight.name_number in {1, 2, 3, 4, 5, 6, 7, 8, 11, 22}
    # Ensure breakdown only contains recognized characters
    assert all(char.isalpha() for char, _ in insight.name_breakdown)
    assert sum(value for _, value in insight.name_breakdown) >= insight.name_number
    assert "name number" in insight.summary.lower()
