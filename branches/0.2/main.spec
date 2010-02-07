# -*- mode: python -*-
a = Analysis([os.path.join(HOMEPATH,'support/_mountzlib.py'), os.path.join(HOMEPATH,'support/useUnicode.py'), './main.py'],
             pathex=['/home/ralsina/trunk/trunk'])

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build/pyi.linux2/main', 'main'),
          debug=False,
          strip=False,
          upx=True,
          console=1 )
          
coll = COLLECT( exe,
               a.binaries,
               [('radios.txt','./radios.txt','DATA')],
               Tree('./icons','icons'),
               Tree('./backgrounds','backgrounds'),
               Tree('./clicks','clicks'),
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name=os.path.join('dist', 'main'))
