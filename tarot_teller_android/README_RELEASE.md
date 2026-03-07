# Tarot Teller Android Release Guide

## 1) Keystore (do not commit)

```bash
keytool -genkeypair -v \
  -keystore keystore/release.keystore \
  -alias tarotteller_release \
  -keyalg RSA -keysize 4096 -validity 3650
```

Add `keystore/` to `.gitignore` (already done).

## 2) Build environment

Use Buildozer with a recent `python-for-android`:

```bash
pip install --upgrade buildozer cython
buildozer android clean
```

## 3) Signing via environment variables

```bash
export KEYSTORE_PATH=keystore/release.keystore
export KEYSTORE_ALIAS=tarotteller_release
export KEYSTORE_PASSWORD='***'
export KEY_PASSWORD='***'
```

## 4) Build release artifacts (APK + AAB)

```bash
buildozer android release
```

Expected artifacts:

- `bin/tarotteller-1.0.0-arm64-v8a-release.apk`
- `bin/tarotteller-1.0.0-arm64-v8a-release.aab`

## 5) Verify target SDK and signing

```bash
aapt dump badging bin/*-release.apk | rg targetSdkVersion
apksigner verify --print-certs bin/*-release.apk
```

## 6) Validate shared tarot image coverage

```bash
python ../scripts/verify_card_assets.py
```

This check fails if any card ID in `app/assets/deck/rider_waite.json` lacks a corresponding image.

## 7) Play upload checklist

- Target SDK: 35
- Permissions: none declared
- Data safety: local-only history
- Upload signed AAB
- Add screenshots, icon assets, feature graphic
