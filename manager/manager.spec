# -*- mode: python -*-
a = Analysis(['RrtMonitor.py'],
             pathex=['C:\\icon'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='RrtMonitor.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False )
