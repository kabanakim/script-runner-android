[app]
title = Script Runner
package.name = scriptrunner
package.domain = org.scriptrunner

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 1.0.0

requirements = python3,kivy==2.1.0

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.arch = armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
