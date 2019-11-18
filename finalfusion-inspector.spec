# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['finalfusion_inspector/__main__.py'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Finalfusion Inspector',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Finalfusion Inspector')

info_plist = {
    "NSHighResolutionCapable": True,
}

app = BUNDLE(coll,
             name='Finalfusion Inspector.app',
             icon="resources/finalfusion.icns",
             bundle_identifier="com.github.finalfusion.inspector",
             info_plist=info_plist)
