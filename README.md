# 🎮 TOKERRGJIK - Ultimate Cross-Platform Edition

**Traditional Albanian Board Game (Nine Men's Morris)**  
Version 11.0 - Python Cross-Platform Edition

![Platforms](https://img.shields.io/badge/platform-Android%20%7C%20iOS%20%7C%20Windows%20%7C%20Linux%20%7C%20macOS%20%7C%20Web-blue)
![Python](https://img.shields.io/badge/python-3.9%2B-green)
![Kivy](https://img.shields.io/badge/kivy-2.3.0-orange)
![License](https://img.shields.io/badge/license-MIT-purple)

---

## 👨‍💻 Developer

**Shaban Ejupi**  
IT Expert & Computer Science Master  
Republic of Kosovo Customs - University of Prishtina

---

## 📱 Platforms

This game runs on **ALL major platforms**:

- 📱 **Android** (APK) - Android 5.0+
- 🍎 **iOS** (IPA) - iOS 11+
- 💻 **Windows** (EXE) - Windows 10+
- 🐧 **Linux** (Native) - All distributions
- 🍎 **macOS** (Native) - macOS 10.14+
- 🌐 **Web** (Browser) - Chrome, Firefox, Safari, Edge

---

## ✨ Features

### 🎮 Game Features
- ✅ **Human vs AI** - Intelligent opponent with 4 difficulty levels
- ✅ **Human vs Human** - Two-player local multiplayer
- ✅ **Undo/Redo System** - Full move history
- ✅ **Auto-Save** - Never lose your progress
- ✅ **Statistics Tracking** - Wins, losses, streaks
- ✅ **Achievements System** - Unlock rewards
- ✅ **Sound Effects** - Premium audio feedback
- ✅ **Modern UI** - Beautiful gradients and animations
- ✅ **Bilingual** - Albanian & English support

### 🤖 AI Features
- **Easy** - 40% error rate, good for beginners
- **Medium** - 20% error rate, balanced gameplay
- **Hard** - 10% error rate, strategic blocking (85%)
- **Expert** - 5% error rate, master level (100% blocking)

### 📊 Statistics
- Win/Loss tracking
- Win streak counter
- Total playtime
- Achievement progress
- Historical data

---

## 🚀 Quick Start

### Desktop (Windows/Linux/macOS)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

### Android APK Build

```bash
# On Linux/macOS (or WSL2 on Windows)
chmod +x build_android.sh
./build_android.sh

# Output: bin/tokerrgjik-11.0-arm64-v8a-debug.apk
```

### Windows EXE Build

```batch
# On Windows
build_windows.bat

# Output: dist/Tokerrgjik.exe
```

### iOS IPA Build

```bash
# On macOS only
chmod +x build_ios.sh
./build_ios.sh

# Opens Xcode project for signing and distribution
```

### Web Version Build

```bash
chmod +x build_web.sh
./build_web.sh

# Output: build/web/
# Test: python -m http.server 8000 --directory build/web
```

---

## 📦 Installation

### Requirements

- **Python 3.9 or higher**
- **pip** (Python package manager)

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Kivy 2.3.0 (GUI framework)
- KivyMD 1.2.0 (Material Design components)
- Pillow 10.3.0 (Image processing)
- Buildozer 1.5.0 (Android builds)
- PyInstaller 6.5.0 (Windows builds)
- Pygbag 0.8.7 (Web builds)

### Step 2: Run the Game

```bash
python main.py
```

---

## 🛠️ Building for Specific Platforms

### 📱 Android (APK)

**Requirements:**
- Linux or macOS (or Windows WSL2)
- Android SDK & NDK (auto-installed by Buildozer)

**Build Commands:**

```bash
# Debug build (for testing)
buildozer android debug

# Release build (for distribution)
buildozer android release

# Deploy to connected device
buildozer android deploy run
```

**Output:**
- `bin/tokerrgjik-11.0-arm64-v8a-debug.apk` (Debug)
- `bin/tokerrgjik-11.0-arm64-v8a-release-unsigned.apk` (Release)

**Sign for Play Store:**

```bash
# Generate keystore
keytool -genkey -v -keystore tokerrgjik.keystore -alias tokerrgjik -keyalg RSA -keysize 2048 -validity 10000

# Sign APK
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore tokerrgjik.keystore bin/tokerrgjik-11.0-arm64-v8a-release-unsigned.apk tokerrgjik

# Align APK
zipalign -v 4 bin/tokerrgjik-11.0-arm64-v8a-release-unsigned.apk bin/tokerrgjik-release.apk
```

### 🍎 iOS (IPA)

**Requirements:**
- macOS with Xcode installed
- Apple Developer Account ($99/year)
- Kivy-iOS toolchain

**Build Commands:**

```bash
# Install Kivy-iOS
git clone https://github.com/kivy/kivy-ios
cd kivy-ios
./toolchain.py build python3 kivy

# Create iOS project
toolchain create Tokerrgjik /path/to/TokerrGjik

# Open in Xcode
cd Tokerrgjik-ios
open Tokerrgjik.xcodeproj
```

**Xcode Steps:**
1. Select your Apple Developer team
2. Configure Bundle Identifier: `com.shabanejupi.tokerrgjik`
3. Connect iOS device
4. Product → Archive
5. Distribute to App Store or TestFlight

### 💻 Windows (EXE)

**Requirements:**
- Windows 10 or higher
- Python 3.9+
- PyInstaller

**Build Commands:**

```batch
# Build EXE
pyinstaller tokerrgjik_windows.spec

# Or use the batch script
build_windows.bat
```

**Output:**
- `dist/Tokerrgjik.exe` (Single executable file)
- Include `dist/` folder contents when distributing

**Create Installer (Optional):**
- Use **Inno Setup** or **NSIS** to create a professional installer

### 🌐 Web Version

**Requirements:**
- Pygbag
- Modern web browser

**Build Commands:**

```bash
# Build web version
pygbag --build main.py

# Test locally
python -m http.server 8000 --directory build/web

# Open browser to http://localhost:8000
```

**Deployment Options:**
- **GitHub Pages** - Free hosting
- **Netlify** - Continuous deployment
- **Vercel** - Edge network
- **Your own server** - Upload `build/web/` folder

---

## 🎯 Game Rules

### Objective
Form "mills" (3 pieces in a row) to remove opponent's pieces. Reduce opponent to 2 pieces or block all their moves to win.

### Phases

#### 1. Placement Phase (9 pieces each)
- Players alternate placing pieces on empty positions
- Form mills to remove opponent's pieces
- Cannot place on occupied positions

#### 2. Movement Phase
- Move pieces to adjacent empty positions
- Form mills to remove opponent's pieces
- When reduced to 3 pieces, enter Flying Phase

#### 3. Flying Phase (≤3 pieces)
- Move to any empty position (not just adjacent)
- More flexible movement options

### Winning
- Reduce opponent to 2 pieces
- Block all opponent's moves

---

## 🎨 Project Structure

```
TokerrGjik/
│
├── main.py                    # Main application entry point
├── game_engine.py             # Core game logic and rules
├── ai_player.py               # AI opponent with multiple difficulties
├── ui_components.py           # Custom Kivy UI widgets
├── score_manager.py           # Score tracking and persistence
├── sound_manager.py           # Audio effects management
│
├── requirements.txt           # Python dependencies
├── buildozer.spec            # Android build configuration
├── tokerrgjik_windows.spec   # Windows build configuration
│
├── build_android.sh          # Android build script
├── build_windows.bat         # Windows build script
├── build_ios.sh              # iOS build script
├── build_web.sh              # Web build script
│
├── sounds/                   # Sound effects (add your own)
│   ├── place.wav
│   ├── move.wav
│   ├── remove.wav
│   ├── mill.wav
│   ├── win.wav
│   └── lose.wav
│
├── assets/                   # Images and icons
│   ├── icon.png
│   ├── icon.ico
│   └── presplash.png
│
└── README.md                 # This file
```

---

## 🔧 Configuration

### Buildozer (Android/iOS)
Edit `buildozer.spec` to customize:
- App name and package
- Version number
- Permissions
- API levels
- Supported architectures

### PyInstaller (Windows)
Edit `tokerrgjik_windows.spec` to customize:
- Include/exclude files
- Icon
- Build options

---

## 📝 Development

### Adding Sound Effects

1. Create `sounds/` directory
2. Add WAV files:
   - `place.wav` - Piece placement
   - `move.wav` - Piece movement
   - `remove.wav` - Piece removal
   - `mill.wav` - Mill formation
   - `win.wav` - Victory
   - `lose.wav` - Defeat
   - `click.wav` - UI click
   - `error.wav` - Error feedback

### Adding Custom Themes

Edit color constants in `ui_components.py` and `main.py`:

```python
PRIMARY_COLOR = (0.1, 0.74, 0.61, 1)  # Turquoise
ACCENT_COLOR = (0.95, 0.77, 0.06, 1)  # Gold
BACKGROUND_COLOR = (0.1, 0.24, 0.31, 1)  # Dark slate
```

### Testing

```bash
# Run on desktop
python main.py

# Test Android on emulator
buildozer android debug deploy run logcat

# Test web version
pygbag --build main.py
python -m http.server 8000 --directory build/web
```

---

## 🐛 Troubleshooting

### Common Issues

**1. Kivy installation fails**
```bash
# On Ubuntu/Debian
sudo apt-get install python3-pip build-essential git python3-dev ffmpeg libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev zlib1g-dev

# Then install Kivy
pip install kivy[full]
```

**2. Buildozer Android build fails**
```bash
# Clear cache and rebuild
buildozer android clean
buildozer android debug
```

**3. PyInstaller EXE doesn't run**
```bash
# Try with console enabled (to see errors)
pyinstaller --console tokerrgjik_windows.spec
```

**4. Web version doesn't load**
- Ensure you're serving via HTTP server (not file://)
- Check browser console for errors
- Try different browser

---

## 📄 License

MIT License - Free to use, modify, and distribute.

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📧 Contact

**Shaban Ejupi**  
Email: [your-email@example.com]  
LinkedIn: [Your LinkedIn]  
GitHub: [Your GitHub]

---

## 🏆 Achievements

Unlock achievements by:
- 🏆 First Victory - Win your first game
- 🔥 Win Streaks - Win 3, 5, or 10 games in a row
- ⭐ Total Wins - Reach 10, 50, or 100 victories
- ⏰ Playtime - Play for 1 hour or 10 hours

---

## 📱 App Store & Play Store

**Coming Soon!**

- [ ] Google Play Store
- [ ] Apple App Store
- [ ] Microsoft Store
- [ ] itch.io (Web version)

---

## 🎉 Version History

### Version 11.0 (Current)
- ✅ Complete Python conversion from Java
- ✅ Cross-platform support (6 platforms)
- ✅ Modern Kivy UI with animations
- ✅ AI opponent with 4 difficulty levels
- ✅ Undo/Redo system
- ✅ Score tracking and achievements
- ✅ Sound effects support
- ✅ Bilingual support (Albanian/English)

### Version 10.0 (Java)
- Original Java Swing version
- Windows-only desktop application

---

## 🙏 Acknowledgments

- **Kivy Team** - Amazing cross-platform framework
- **Albanian Culture** - Traditional game preservation
- **Open Source Community** - Tools and libraries

---

**🎮 Enjoy playing Tokerrgjik! 🏆**

Made with ❤️ in Kosovo 🇽🇰
