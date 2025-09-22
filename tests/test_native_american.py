from datetime import date

from tarot_teller.native_american import totem_for


def test_totem_wraparound():
    goose = totem_for(date(1990, 1, 15))
    otter = totem_for(date(1990, 1, 25))

    assert goose.totem == "Goose"
    assert otter.totem == "Otter"
