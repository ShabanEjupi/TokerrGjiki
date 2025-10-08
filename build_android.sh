#!/bin/bash

# Build script for Android APK using Buildozer
# Run this on Linux or macOS

echo "🚀 Building Tokerrgjik for Android..."
echo "====================================="

# Check if buildozer is installed
if ! command -v buildozer &> /dev/null
then
    echo "❌ Buildozer not found. Installing..."
    pip install buildozer cython
fi

# Check if running on supported OS
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo "⚠️  Windows detected. Please use WSL2 or Linux for Android builds."
    echo "   Or use GitHub Actions / CI/CD pipeline."
    exit 1
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
buildozer android clean

# Build APK in debug mode
echo "📦 Building APK (Debug)..."
buildozer android debug

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo "📱 APK location: bin/tokerrgjik-11.0-arm64-v8a-debug.apk"
    echo ""
    echo "To install on device:"
    echo "  adb install bin/tokerrgjik-11.0-arm64-v8a-debug.apk"
    echo ""
    echo "To build release version:"
    echo "  buildozer android release"
else
    echo "❌ Build failed. Check errors above."
    exit 1
fi
