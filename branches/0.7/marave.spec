# -*- mode: python -*-
a = Analysis([os.path.join(HOMEPATH,'support/_mountzlib.py'), os.path.join(HOMEPATH,'support/useUnicode.py'), 'marave/main.py'],
             pathex=['/home/ralsina/trunk/trunk'])

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build/pyi.linux2/main', 'marave.exe'),
          debug=False,
          strip=False,
          upx=True,
          console=0 )
          
coll = COLLECT( exe,
               a.binaries,
               [('radios.txt','marave/radios.txt','DATA')],
               Tree('marave/icons','icons'),
               Tree('marave/backgrounds','backgrounds'),
               Tree('marave/clicks','clicks'),
               Tree('marave/stylesheets','stylesheets'),
               Tree('marave/themes','themes'),
               Tree('marave/translations','translations'),
               Tree('marave/highlight','highlight'),
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name=os.path.join('dist', 'marave'))
