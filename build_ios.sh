#!/bin/bash

# Build script for iOS IPA using Kivy-iOS
# Run this on macOS only

echo "🍎 Building Tokerrgjik for iOS..."
echo "====================================="

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ This script must run on macOS for iOS builds."
    exit 1
fi

# Check if kivy-ios is installed
if ! command -v toolchain &> /dev/null
then
    echo "❌ Kivy-iOS toolchain not found. Installing..."
    echo "This may take a while..."
    
    # Install dependencies
    brew install autoconf automake libtool pkg-config
    brew link libtool
    
    # Clone and install kivy-ios
    git clone https://github.com/kivy/kivy-ios
    cd kivy-ios
    ./toolchain.py build python3 kivy
    cd ..
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf ios-build

# Create Xcode project
echo "📦 Creating iOS project..."
toolchain create Tokerrgjik ~/path/to/TokerrGjik

# Build for iOS
echo "🔨 Building for iOS..."
cd Tokerrgjik-ios

# Open Xcode project
echo "✅ iOS project created!"
echo "📱 Opening Xcode..."
echo ""
echo "Next steps:"
echo "1. Open Tokerrgjik.xcodeproj in Xcode"
echo "2. Select your development team"
echo "3. Connect your iOS device"
echo "4. Build and run (Cmd + R)"
echo ""
echo "To create an IPA for App Store:"
echo "1. Product > Archive"
echo "2. Distribute App"
echo "3. Follow App Store Connect workflow"

open Tokerrgjik.xcodeproj
