# -*- mode: python -*-
a = Analysis(['monitor.py'],
             pathex=['F:\\rrtmonitor\\monitor'],
             hiddenimports=['pymssql','_mssql','uuid'],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='monitor.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False )
