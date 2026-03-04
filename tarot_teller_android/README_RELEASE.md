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

Use Buildozer with a recent `python-for-android` (develop branch if needed for API 35 compatibility):

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

Build command:

```bash
buildozer android release
```

Expected artifact:

`bin/TarotTeller-1.0.0-arm64-v8a-release.aab`

## 4) Verify manifest targets API 35

```bash
aapt dump badging bin/*.aab | rg targetSdkVersion
```

## 5) Play upload checklist

- Target SDK: 35
- Permissions: none declared
- Data safety: local-only history
- Upload signed AAB
- Add screenshots, icon assets, feature graphic
