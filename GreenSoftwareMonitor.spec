# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[('/home/bian/.wine/drive_c/windows/system32/vcruntime140.dll', '.'), ('/home/bian/.wine/drive_c/windows/system32/msvcp140.dll', '.')],
    datas=[('assets/*', 'assets'), ('fonts/*', 'fonts')],
    hiddenimports=['psutil', 'PIL', 'proyectoco2'],
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
    name='GreenSoftwareMonitor',
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
    name='GreenSoftwareMonitor',
)
