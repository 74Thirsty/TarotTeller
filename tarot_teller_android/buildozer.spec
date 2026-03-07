[app]
title = Tarot Teller
package.name = tarotteller
package.domain = io.tarotteller
source.dir = app
source.include_exts = py,kv,json,png,webp,ttf,md,txt
# force python-for-android to use a compatible cython
p4a.extra_args = --cython=0.29.36
version = 1.0.0

requirements = python3,kivy,kivymd,pyjnius==1.6.1


orientation = portrait
fullscreen = 0

android.permissions =

android.api = 35
android.minapi = 24
android.release_artifact = apk,aab
android.archs = arm64-v8a
android.add_assets = app/assets@assets

[buildozer]
log_level = 2
warn_on_root = 1


