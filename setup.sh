#!/bin/bash

# Quick setup script for Tokerrgjik on Linux/macOS

echo "========================================"
echo "TOKERRGJIK - Setup Script"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ ERROR: Python 3 is not installed!"
    echo ""
    echo "Install Python:"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "  Fedora: sudo dnf install python3 python3-pip"
    echo "  macOS: brew install python3"
    exit 1
fi

echo "✅ Python found:"
python3 --version
echo ""

# Check pip
if ! command -v pip3 &> /dev/null
then
    echo "❌ pip not found. Installing..."
    python3 -m ensurepip --upgrade
fi

# Upgrade pip
echo "⬆️  Upgrading pip..."
python3 -m pip install --upgrade pip

# Install requirements
echo ""
echo "📦 Installing dependencies..."
echo "This may take a few minutes..."
echo ""
python3 -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ ERROR: Failed to install dependencies!"
    echo ""
    echo "Try:"
    echo "  sudo pip3 install -r requirements.txt"
    exit 1
fi

# Create directories
echo ""
echo "📁 Creating directories..."
mkdir -p sounds
mkdir -p assets

# Make build scripts executable
chmod +x build_android.sh
chmod +x build_ios.sh
chmod +x build_web.sh

echo ""
echo "========================================"
echo "✅ Setup Complete!"
echo "========================================"
echo ""
echo "To run the game:"
echo "  python3 main.py"
echo ""
echo "To build for different platforms:"
echo "  Android: ./build_android.sh"
echo "  iOS:     ./build_ios.sh (macOS only)"
echo "  Web:     ./build_web.sh"
echo ""
echo "For Windows EXE:"
echo "  Use Windows and run build_windows.bat"
echo ""
echo "For more information, see README.md"
echo ""
