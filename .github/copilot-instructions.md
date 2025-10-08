# Tokerrgjik Game - Copilot Instructions

<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

## Project Overview
This is a Python-based traditional Albanian board game (Tokerrgjik/Nine Men's Morris) with cross-platform support.

## Technology Stack
- **Framework**: Kivy (cross-platform GUI)
- **Language**: Python 3.9+
- **Build Tools**: Buildozer (Android), Kivy-iOS (iOS), PyInstaller (Windows), Pygbag (Web)

## Code Style Guidelines
- Follow PEP 8 Python style guide
- Use type hints for function parameters and return values
- Document all classes and complex functions with docstrings
- Keep functions focused and single-purpose
- Use meaningful variable names in both Albanian and English

## Game Architecture
- `main.py` - Entry point and Kivy app initialization
- `game_engine.py` - Core game logic and rules
- `ai_player.py` - AI opponent with multiple difficulty levels
- `ui_components.py` - Custom UI widgets and animations
- `score_manager.py` - Persistent score tracking
- `sound_manager.py` - Audio effects and music

## Cross-Platform Considerations
- Use Kivy's platform-agnostic widgets
- Handle touch and mouse events uniformly
- Optimize for both desktop and mobile screen sizes
- Test on multiple resolutions and aspect ratios

## Build System
- Each platform has dedicated build configuration
- Automated scripts for one-command builds
- Version management across all platforms

## Albanian Language Support
- All UI text should be bilingual (Albanian/English)
- Use Unicode properly for Albanian characters (ë, ç)
- Consider RTL support for future expansion
