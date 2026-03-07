from pathlib import Path

from tarotteller.core.card_images import card_image_id, resolve_card_image
<<<<<<< ours
=======
from tarotteller.interfaces.gui import _preview_subsample_factor
>>>>>>> theirs


def test_card_image_id_normalization() -> None:
    assert card_image_id("The High Priestess") == "the_high_priestess"
    assert card_image_id("Seven-of-Wands") == "seven_of_wands"


def test_resolve_card_image_handles_unknown_card() -> None:
    path = resolve_card_image("not a real card")
    assert path is None or isinstance(path, Path)
<<<<<<< ours
=======


def test_preview_subsample_factor_keeps_card_within_bounds() -> None:
    assert _preview_subsample_factor(110, 160) == 1
    assert _preview_subsample_factor(660, 960) == 3
    assert _preview_subsample_factor(300, 1200) == 4
>>>>>>> theirs
