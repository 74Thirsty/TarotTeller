from pathlib import Path

from tarotteller.core.card_images import card_image_id, resolve_card_image


def test_card_image_id_normalization() -> None:
    assert card_image_id("The High Priestess") == "the_high_priestess"
    assert card_image_id("Seven-of-Wands") == "seven_of_wands"


def test_resolve_card_image_handles_unknown_card() -> None:
    path = resolve_card_image("not a real card")
    assert path is None or isinstance(path, Path)
