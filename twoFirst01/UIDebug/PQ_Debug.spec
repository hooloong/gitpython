# -*- mode: python -*-

block_cipher = None


a = Analysis(['PQ_Debug.py'],
             pathex=['D:\\vault\\PQ_Tool\\SX8\\UIDebug'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=True,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='PQ_Debug',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='222.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='PQ_Debug')
