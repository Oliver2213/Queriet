# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['c:\\code\\queriet\\queriet'],
             binaries=None,
             datas=[('queriet.confspec', '.')],
             hiddenimports=['requests', 'vocabulary'],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             win_no_prefer_redirects=None,
             win_private_assemblies=None,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='queriet',
          debug=False,
          strip=None,
          upx=True,
          console=False )
