# Tarot Teller Android (Kivy + Buildozer)

This folder contains an Android-targeted Kivy app with a pure-Python tarot engine.

## Highlights

- Offline deck data + text-only image specifications (Section X compliant)
- Deterministic seeded reading engine
- Supported spreads: Daily Draw, 3-card, Yes/No, Celtic Cross
- Local JSON history + searchable history view
- No dangerous permissions declared
- Buildozer config for AAB release targeting API 35

## Run engine tests

```bash
cd tarot_teller_android/app
pytest tests/test_reading_engine.py
```

## Build Android AAB

See `README_RELEASE.md` for signing and release commands.



## Image assets

`app/assets/deck/images` is the shared source of truth for card images across:
- Android app packaging
- iOS asset import pipeline (same card ID filenames)
- Desktop/Tkinter preview rendering

Run `python ../scripts/verify_card_assets.py` before releases to ensure all 78 IDs in `rider_waite.json` resolve to image files.
