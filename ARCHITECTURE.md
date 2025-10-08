# 🏗️ Tokerrgjik Architecture

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     TOKERRGJIK GAME                         │
│                  Cross-Platform Edition                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │         main.py (Entry Point)           │
        │    - TokerrgjikApp (Kivy App)          │
        │    - Screen Manager                     │
        │    - Global State Management            │
        └──────────────┬──────────────────────────┘
                       │
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
    ┌────────┐   ┌────────┐   ┌──────────┐
    │ Screens│   │  Core  │   │Managers  │
    └────────┘   └────────┘   └──────────┘
         │            │             │
    ┌────┴────┐  ┌───┴────┐   ┌────┴─────┐
    ▼         ▼  ▼        ▼   ▼          ▼
┌───────┐ ┌────┐┌────┐┌───┐┌────┐  ┌─────┐
│ Main  │ │Game││Stat││Set││Help│  │Score│
│ Menu  │ │    ││    ││   ││    │  │     │
└───────┘ └────┘└────┘└───┘└────┘  └─────┘
              │
         ┌────┴──────┐
         ▼           ▼
    ┌────────┐  ┌───────┐
    │ Game   │  │  AI   │
    │ Engine │  │Player │
    └────────┘  └───────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐┌──────┐
│UI Comp││Sound │
└────────┘└──────┘
```

## Component Details

### 🎮 Main Application Layer
**File:** `main.py`
- Kivy App initialization
- Screen management
- Global state coordination
- Platform detection

### 🧠 Core Game Logic
**File:** `game_engine.py`
- Board state management
- Move validation
- Mill detection
- Win condition checking
- Undo/Redo system
- Game phases (placement, movement, flying)

### 🤖 AI System
**File:** `ai_player.py`
- 4 difficulty levels (Easy, Medium, Hard, Expert)
- Strategic move selection
- Mill formation priority
- Opponent blocking logic
- Position evaluation

### 🎨 UI Components
**File:** `ui_components.py`
- ModernButton (styled buttons)
- GameBoard (interactive board widget)
- ScorePanel (score display)
- MenuBar (status bar)
- Custom animations

### 💾 Data Management
**Files:** `score_manager.py`, `sound_manager.py`
- Persistent score storage
- Achievement tracking
- Sound effect playback
- Settings management

---

## Data Flow

```
User Input (Touch/Click)
         │
         ▼
   GameBoard Widget
         │
         ▼
   Game Engine (Validate)
         │
    ┌────┴────┐
    ▼         ▼
Update UI   Check Win
    │         │
    ▼         ▼
Redraw    Save Score
```

---

## Build System Architecture

```
┌────────────────────────────────────────┐
│          Source Code (Python)          │
│     main.py + game modules             │
└─────────────┬──────────────────────────┘
              │
    ┌─────────┼─────────┬──────────┬──────────┐
    ▼         ▼         ▼          ▼          ▼
┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐
│Android ││  iOS   ││Windows ││  Web   ││Desktop │
│ APK    ││  IPA   ││  EXE   ││ HTML5  ││ Native │
└────────┘└────────┘└────────┘└────────┘└────────┘
    │         │         │          │          │
    ▼         ▼         ▼          ▼          ▼
Buildozer Kivy-iOS PyInstaller Pygbag   Python
```

---

## Platform-Specific Layers

### Android (Buildozer)
```
Python Code → Cython → Android NDK → APK
```

### iOS (Kivy-iOS)
```
Python Code → Cython → iOS SDK → IPA
```

### Windows (PyInstaller)
```
Python Code → Bytecode → Bundled → EXE
```

### Web (Pygbag)
```
Python Code → WebAssembly → Browser
```

---

## File Dependencies

```
main.py
├── game_engine.py
├── ai_player.py (uses game_engine)
├── ui_components.py (uses game_engine)
├── score_manager.py
└── sound_manager.py

game_engine.py
└── (standalone, no dependencies)

ai_player.py
└── game_engine.py

ui_components.py
└── game_engine.py

score_manager.py
└── (standalone, uses Kivy storage)

sound_manager.py
└── (standalone, uses Kivy audio)
```

---

## Game State Machine

```
        ┌──────────┐
        │  START   │
        └────┬─────┘
             ▼
      ┌──────────────┐
      │  PLACEMENT   │ (18 pieces to place)
      │    PHASE     │
      └──────┬───────┘
             ▼
      ┌──────────────┐
      │  MOVEMENT    │ (>3 pieces each)
      │    PHASE     │
      └──────┬───────┘
             ▼
      ┌──────────────┐
      │   FLYING     │ (≤3 pieces)
      │    PHASE     │
      └──────┬───────┘
             ▼
        ┌──────────┐
        │GAME OVER │
        └──────────┘
```

---

## AI Decision Tree

```
AI Turn
  │
  ├─> Removal Phase?
  │   ├─> Remove strategic piece
  │   └─> Update board
  │
  ├─> Placement Phase?
  │   ├─> Can form mill? → Place there
  │   ├─> Block opponent mill? → Place there
  │   ├─> Strategic position? → Place there
  │   └─> Random valid position
  │
  └─> Movement Phase?
      ├─> Can form mill? → Move there
      ├─> Block opponent? → Move there
      ├─> Strategic position? → Move there
      └─> Random valid move
```

---

## Memory Management

```
Game State (Undo/Redo)
  │
  ├─> History Stack (past states)
  ├─> Redo Stack (undone states)
  └─> Current State (active game)

Persistent Storage
  │
  ├─> Scores (JSON)
  ├─> Achievements (JSON)
  └─> Settings (JSON)
```

---

## Performance Optimization

### Desktop
- Native Python execution
- OpenGL rendering (Kivy)
- 60 FPS animations

### Mobile
- Compiled to native code (Cython)
- GPU-accelerated graphics
- Touch-optimized

### Web
- WebAssembly compilation
- Browser-native rendering
- Progressive loading

---

## Security Features

### Anti-Cheat (from Java version)
- Move validation server-side
- State verification
- History tracking

### Data Protection
- Encrypted score storage
- Tamper detection
- Input sanitization

---

## Scalability

### Current Support
- Single device gameplay
- Local scores

### Future Expansion
- Online multiplayer
- Cloud saves
- Leaderboards
- In-app purchases
- Achievements sync

---

## Testing Strategy

```
Unit Tests
├── game_engine_test.py
├── ai_player_test.py
└── score_manager_test.py

Integration Tests
├── gameplay_test.py
└── ui_test.py

Platform Tests
├── android_test.apk
├── ios_test.ipa
├── windows_test.exe
└── web_test.html
```

---

## Deployment Pipeline

```
Git Push
    ↓
GitHub Actions
    ↓
┌───────────────────┐
│  Build Matrix     │
├───────────────────┤
│ • Android APK     │
│ • Windows EXE     │
│ • Web Version     │
└─────────┬─────────┘
          ↓
    Artifacts Ready
          ↓
    Auto-Deploy
    (optional)
```

---

## Code Organization

```
TokerrGjik/
├── 📱 App Layer (main.py)
│   └── Screen management, navigation
│
├── 🎮 Game Layer (game_engine.py)
│   └── Rules, logic, validation
│
├── 🤖 AI Layer (ai_player.py)
│   └── Decision making, strategy
│
├── 🎨 Presentation Layer (ui_components.py)
│   └── Widgets, animations, drawing
│
└── 💾 Data Layer (managers)
    ├── Scores & achievements
    └── Sound & settings
```

---

## Summary

**Clean Architecture:**
- ✅ Separation of concerns
- ✅ Modular design
- ✅ Easy to test
- ✅ Easy to maintain
- ✅ Easy to extend

**Cross-Platform:**
- ✅ Single codebase
- ✅ Platform-specific builds
- ✅ Native performance
- ✅ Consistent UX

**Production Ready:**
- ✅ Error handling
- ✅ State management
- ✅ Data persistence
- ✅ CI/CD pipeline

---

*Architecture designed for scalability and maintainability*
