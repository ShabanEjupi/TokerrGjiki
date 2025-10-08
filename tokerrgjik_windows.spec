# -*- mode: python ; coding: utf-8 -*-

"""
PyInstaller spec file for Windows EXE build
Build command: pyinstaller tokerrgjik_windows.spec
"""

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('sounds', 'sounds'),
        ('assets', 'assets'),
    ],
    hiddenimports=[
        'kivy',
        'kivymd',
        'PIL',
        'game_engine',
        'ai_player',
        'ui_components',
        'score_manager',
        'sound_manager'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Tokerrgjik',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None  # Icon file - add assets/icon.ico when ready
)
