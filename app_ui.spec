# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs, collect_submodules

datas = [('mh_script/resource', 'resource')]
hiddenimports = []

datas += collect_data_files('Cython')
datas += collect_data_files('paddleocr', include_py_files=True)

hiddenimports += collect_submodules('paddleocr')
hiddenimports += collect_submodules('mss')
hiddenimports += collect_submodules('pygetwindow')
hiddenimports += collect_submodules('pyautogui')

binaries = collect_dynamic_libs('paddle')

a = Analysis(
    ['app_ui.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
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
    name='app_ui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='app_ui',
)
