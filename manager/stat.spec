# -*- mode: python -*-
a = Analysis(['stat.py'],
             pathex=['F:\\rrtmonitor\\manager'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='stat.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
