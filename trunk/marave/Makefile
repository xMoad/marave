
all: icons_rc.py Ui_searchreplacewidget.py Ui_searchwidget.py \
     Ui_prefs.py README.html 

icons_rc.py: icons.qrc
	pyrcc4 icons.qrc -o icons_rc.py

Ui_searchreplacewidget.py: searchreplwidget.ui
	pyuic4 searchreplwidget.ui -o Ui_searchreplacewidget.py -x

Ui_searchwidget.py: searchwidget.ui
	pyuic4 searchwidget.ui -o Ui_searchwidget.py -x

Ui_prefs.py: prefs.ui
	pyuic4 prefs.ui -o Ui_prefs.py -x


README.html: ../README
	rst2html ../README README.html

translations: force
	pylupdate4 *py -ts translations/*.ts
	cd translations ; make

force:
	true
