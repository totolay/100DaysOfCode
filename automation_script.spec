# -*- mode: python ; coding: utf-8 -*-
import os


a = Analysis(
    ['automation_script.py'],
    pathex=[os.getcwd()],
    binaries=[],
datas=[('gui_config.json', '.'), ('automation_script.spec', '.'), ('images/Screenshot 2025-03-18 153217.png', '.'), ('images/Screenshot 2025-03-18 153233.png', '.'), ('images/Screenshot 2025-03-18 153249.png', '.'), ('images/Screenshot 2025-03-19 093109.png', '.'), ('images/Screenshot 2025-03-19 200031 - Copy.png', '.'), ('images/Screenshot 2025-03-19 200031.png', '.'), ('images/screenshot.png', '.')],
    hiddenimports=["cv2", "pyautogui", "pygetwindow", "tkinter"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='automation_script',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='automation_script',
)
