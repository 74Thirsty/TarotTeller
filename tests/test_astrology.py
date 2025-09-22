from datetime import date

from tarot_teller.astrology import chinese_zodiac_for, western_zodiac_for


def test_western_zodiac_boundaries():
    assert western_zodiac_for(date(1990, 3, 21)).sign == "Aries"
    assert western_zodiac_for(date(1990, 4, 19)).sign == "Aries"
    assert western_zodiac_for(date(1990, 4, 20)).sign == "Taurus"


def test_chinese_zodiac_cycle():
    assert chinese_zodiac_for(date(1996, 7, 12)).animal == "Rat"
    assert chinese_zodiac_for(date(1997, 7, 12)).animal == "Ox"
