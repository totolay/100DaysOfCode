# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['gui_config.py'],
    pathex=[],
    binaries=[],
    datas=[('gui_config.json', '.'), ('automation_script.spec', '.'), ('Screenshot 2025-03-18 153217.png', '.'), ('Screenshot 2025-03-18 153233.png', '.'), ('Screenshot 2025-03-18 153249.png', '.'), ('Screenshot 2025-03-19 093109.png', '.'), ('Screenshot 2025-03-19 200031 - Copy.png', '.'), ('Screenshot 2025-03-19 200031.png', '.'), ('screenshot.png', '.')],
    hiddenimports=["tkinter", "json", "os", "subprocess", "pyautogui", "cv2", "numpy", "time", "pygetwindow", "shutil", "pathlib"],
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
    a.binaries,
    a.datas,
    [],
    name='gui_config',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
