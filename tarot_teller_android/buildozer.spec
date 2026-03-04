[app]
title = Tarot Teller
package.name = tarotteller
package.domain = com.yourcompany
source.dir = app
source.include_exts = py,kv,json,png,webp,ttf

version = 1.0.0

requirements = python3,kivy,kivymd

orientation = portrait
fullscreen = 0

android.permissions =

android.api = 35
android.minapi = 24
android.release_artifact = aab
android.archs = arm64-v8a
android.add_assets = app/assets@assets

[buildozer]
log_level = 2
warn_on_root = 1
