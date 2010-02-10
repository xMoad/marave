REM c:\Python26\python.exe pyinstaller\Configure.py

rd dist /s /q
c:\Python26\python.exe pyinstaller\Build.py marave.spec
rd dist\marave\backgrounds\.svn /s /q
rd dist\marave\themes\.svn /s /q
rd dist\marave\sylesheets\.svn /s /q
rd dist\marave\clicks\.svn /s /q
rd dist\marave\icons\.svn /s /q

"c:\Program Files\NSIS\makensisw.exe" marave.nsi