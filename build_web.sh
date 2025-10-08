#!/bin/bash

# Build script for Web version using Pygbag
# Creates a web-playable version that runs in browsers

echo "🌐 Building Tokerrgjik for Web..."
echo "====================================="

# Check if pygbag is installed
if ! command -v pygbag &> /dev/null
then
    echo "❌ Pygbag not found. Installing..."
    pip install pygbag
fi

# Create web build
echo "📦 Building web version..."
pygbag --build main.py

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo "🌐 Web version created in: build/web"
    echo ""
    echo "To test locally:"
    echo "  python -m http.server 8000 --directory build/web"
    echo "  Then open: http://localhost:8000"
    echo ""
    echo "To deploy:"
    echo "  Upload the build/web folder to your web host"
    echo "  Or use GitHub Pages, Netlify, Vercel, etc."
else
    echo "❌ Build failed. Check errors above."
    exit 1
fi
