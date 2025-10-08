# 🚀 Quick Start Guide

## 5-Minute Setup

### Step 1: Install Python
Download and install Python 3.9+ from [python.org](https://www.python.org/downloads/)

### Step 2: Run Setup
**Windows:**
```batch
setup.bat
```

**Linux/macOS:**
```bash
chmod +x setup.sh
./setup.sh
```

### Step 3: Play!
```bash
python main.py
```

---

## Building for Platforms

### 📱 Android APK
**Linux/macOS/WSL2:**
```bash
./build_android.sh
```
Output: `bin/tokerrgjik-11.0-arm64-v8a-debug.apk`

### 💻 Windows EXE
**Windows:**
```batch
build_windows.bat
```
Output: `dist/Tokerrgjik.exe`

### 🌐 Web Version
```bash
./build_web.sh
python -m http.server 8000 --directory build/web
```
Open: http://localhost:8000

### 🍎 iOS (macOS only)
```bash
./build_ios.sh
```
Opens Xcode for final build and signing.

---

## VS Code Tasks

Press `Ctrl+Shift+B` (Windows/Linux) or `Cmd+Shift+B` (macOS) to see:

1. **Run Tokerrgjik Game** - Launch the game
2. **Setup - Install Dependencies** - Install Python packages
3. **Build - Windows EXE** - Build Windows executable
4. **Build - Android APK** - Build Android app
5. **Build - Web Version** - Build web version
6. **Test - Local Web Server** - Test web version
7. **Clean Build Artifacts** - Clean build files

---

## Debugging

Press `F5` or go to **Run > Start Debugging** to:
- Run with debugger attached
- Set breakpoints
- Inspect variables
- Step through code

---

## File Structure

```
📁 Project Root
├── 🎮 main.py - Run this to play!
├── 🧠 game_engine.py - Game logic
├── 🤖 ai_player.py - AI opponent
├── 🎨 ui_components.py - UI widgets
├── 💾 score_manager.py - Save scores
├── 🔊 sound_manager.py - Sound effects
│
├── 📦 requirements.txt - Dependencies
├── ⚙️ buildozer.spec - Android config
├── ⚙️ tokerrgjik_windows.spec - Windows config
│
├── 🔨 build_android.sh - Build Android
├── 🔨 build_windows.bat - Build Windows
├── 🔨 build_ios.sh - Build iOS
├── 🔨 build_web.sh - Build Web
│
├── 🔧 setup.bat - Windows setup
├── 🔧 setup.sh - Linux/macOS setup
│
├── 📖 README.md - Full documentation
└── 📖 QUICKSTART.md - This file
```

---

## Troubleshooting

### Game won't run?
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check Python version (must be 3.9+)
python --version
```

### Android build fails?
- Use Linux or macOS (or WSL2 on Windows)
- Buildozer needs time (~30 min first build)
- Check internet connection

### Windows EXE build fails?
```batch
# Install PyInstaller
pip install pyinstaller

# Try building manually
pyinstaller tokerrgjik_windows.spec
```

### Web version doesn't work?
- Must use HTTP server (not file://)
- Check browser console for errors
- Try different browser

---

## Next Steps

1. ✅ Run the game: `python main.py`
2. 🎮 Play a game against AI
3. 📊 Check your statistics
4. 🔨 Build for your platform
5. 📱 Share with friends!

---

## Need Help?

- 📖 Full docs: See **README.md**
- 🐛 Issues: Open GitHub issue
- 💬 Questions: Contact developer

---

**Enjoy Tokerrgjik! 🎮🏆**
