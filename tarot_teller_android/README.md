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

This repo revision intentionally avoids committing binary image files.
See `app/assets/deck/images/IMAGE_SPECS.md` and `../release/IMAGE_SPECS.md` for production asset requirements.
