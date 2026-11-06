[app]
title = Calculus Jetpack
package.name = calculusjetpack
package.domain = org.codexgames
source.dir = .
source.include_exts = py,kv,png,jpg,atlas
version = 1.0
requirements = python3,kivy
orientation = landscape
fullscreen = 1

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.api = 35
android.minapi = 23
android.archs = arm64-v8a
android.accept_sdk_license = True
