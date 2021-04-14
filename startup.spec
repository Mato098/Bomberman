# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [('other_textures', 'other_textures'), ('sound', 'sound'), ('bomb_sprites', 'bomb_sprites'),
('bomberman_sprites', 'bomberman_sprites'), ('explosion_sprites', 'explosion_sprites'), ('multiplayer_settings', 'multiplayer_settings')]

a = Analysis(['startup.py'],
             pathex=['C:\\Users\\Martin\\PycharmProjects\\python veci\\Bomberman'],
             binaries=[],
             datas=added_files,
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='startup',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
