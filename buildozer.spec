[app]
# Application title
title = Tokerrgjik

# Package name
package.name = tokerrgjik

# Package domain (used for Android/iOS)
package.domain = com.shabanejupi

# Source code directory
source.dir = .

# Source files to include
source.include_exts = py,png,jpg,kv,atlas,wav,mp3,ogg

# Version
version = 11.0

# Application requirements
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,android

# Orientation (landscape, portrait, all)
orientation = landscape

# Fullscreen mode
fullscreen = 0

# Presplash
#presplash.filename = %(source.dir)s/assets/presplash.png

# Icon
#icon.filename = %(source.dir)s/assets/icon.png

# Supported orientations
android.orientation = landscape

# Android permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Android API
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33

# Android architecture
android.archs = arm64-v8a,armeabi-v7a

# Android features
android.features = android.hardware.touchscreen

# Android services
#android.services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

# Bootstrap
#p4a.bootstrap = sdl2

# Accept Android SDK license
android.accept_sdk_license = True

# Skip update of sdk and ndk
android.skip_update = False

# Gradle dependencies
android.gradle_dependencies = 

# Add Java classes
#android.add_src = 

# App theme
#android.apptheme = "@android:style/Theme.NoTitleBar"

# Copy library
#android.add_libs_armeabi_v7a = libs/android/*.so

# Whitelist
#android.whitelist = lib-dynload/_csv.so

# Python for android directory
#p4a.source_dir = 

# P4A local recipes
#p4a.local_recipes = 

# P4A hooks
#p4a.hook = 

# P4A extra arguments
#p4a.extra_args = 

# iOS specific settings
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0

# iOS Codesign
#ios.codesign.allowed = true

# Log level
log_level = 2

# Warning on backspace
warn_on_root = 1
