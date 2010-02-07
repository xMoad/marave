#-*- coding: utf-8 -*-

"""The user interface for our app"""

# Marave, a relaxing text editor.
# Copyright (C) 2010 Roberto Alsina <ralsina@netmanagers.com.ar>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import os,sys,codecs,re

if hasattr(sys, 'frozen'):
    PATH = os.path.abspath(os.path.dirname(sys.executable))
else:
    PATH = os.path.abspath(os.path.dirname(__file__))

# Import Qt modules
from PyQt4 import QtCore,QtGui
from PyQt4.phonon import Phonon

try:
    import enchant
    from spelltextedit import SpellTextEdit as EditorClass
    print 'Spellchecking available'
except ImportError:
    EditorClass=QtGui.QPlainTextEdit
    print 'Spellchecking disabled'

from Ui_searchwidget import Ui_Form as UI_SearchWidget
from Ui_searchreplacewidget import Ui_Form as UI_SearchReplaceWidget
from Ui_searchreplacewidget import Ui_Form as UI_SearchReplaceWidget
from Ui_prefs import Ui_Form as UI_Prefs

class animatedOpacity:
    def moveOpacity(self):
        if abs(abs(self.proxy.opacity())-abs(self.targetOpacity))<.1:
            self.proxy.setOpacity(self.targetOpacity)
            if self.targetOpacity==0:
                self.hide()
            self.movingOp=False
        else:
            self.show()
            self.movingOp=True
            if self.proxy.opacity()<self.targetOpacity:
                self.proxy.setOpacity(self.proxy.opacity()+.1)
            else:
                self.proxy.setOpacity(self.proxy.opacity()-.1)
            QtCore.QTimer.singleShot(10,self.moveOpacity)

    def showChildren(self):
        for c in self.children:
            c.targetOpacity=.8
            c.moveOpacity()

    def hideChildren(self):
        for c in self.children:
            c.targetOpacity=0.
            c.moveOpacity()

class Handle(QtGui.QGraphicsRectItem, animatedOpacity):
    def __init__(self,x,y,w,h):
        QtGui.QGraphicsRectItem.__init__(self,x,y,w,h)
        self.setBrush(QtGui.QColor(100,100,100,80))
        self.setPen(QtGui.QColor(0,0,0,0))
        self.targetOpacity=0
        self.proxy=self
        self.children=[]

class PrefsWidget(QtGui.QWidget, animatedOpacity):
    def __init__(self, scene, opacity=0):
        QtGui.QWidget.__init__(self)
        # Set up the UI from designer
        self.ui=UI_Prefs()
        self.baseOpacity=opacity
        self.proxy=scene.addWidget(self)
        self.proxy.setOpacity(opacity)
        self.movingOp=False
        self.children=[]
        self.ui.setupUi(self)
        self.loadthemelist()
        self.loadSpellcheckers()
        self.proxy.setZValue(100)

    def loadSpellcheckers(self):
        self.ui.langBox.clear()
        self.ui.langBox.addItem('None')
        try:
            import enchant
            for l, _ in enchant.Broker().list_dicts():
                self.ui.langBox.addItem(l)
        except ImportError:
            self.ui.langBox.setEnabled(False)
        
    def loadthemelist(self):
        self.ui.themeList.clear()
        self.ui.themeList.addItem('')
        tdir=os.path.join(PATH,'themes')
        for t in os.listdir(tdir):
            if t.startswith('.'):
                continue
            self.ui.themeList.addItem(t)
        

class SearchWidget(QtGui.QWidget, animatedOpacity):
    def __init__(self, scene, opacity=0):
        QtGui.QWidget.__init__(self)
        # Set up the UI from designer
        self.ui=UI_SearchWidget()
        self.baseOpacity=opacity
        self.proxy=scene.addWidget(self)
        self.proxy.setOpacity(opacity)
        self.movingOp=False
        self.children=[]
        self.ui.setupUi(self)
        self.proxy.setZValue(100)


class SearchReplaceWidget(QtGui.QWidget, animatedOpacity):
    def __init__(self, scene, opacity=0):
        QtGui.QWidget.__init__(self)
        # Set up the UI from designer
        self.ui=UI_SearchReplaceWidget()
        self.baseOpacity=opacity
        self.proxy=scene.addWidget(self)
        self.proxy.setOpacity(opacity)
        self.movingOp=False
        self.children=[]
        self.ui.setupUi(self)
        self.proxy.setZValue(100)


class FunkyLabel(QtGui.QLabel, animatedOpacity):
    def __init__(self, text, scene,opacity=.3):
        QtGui.QLabel.__init__(self,text)
        self.baseOpacity=opacity
        self.proxy=scene.addWidget(self)
        self.proxy.setOpacity(opacity)
        self.movingOp=False
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.children=[]
        self.setStyleSheet("""
                              padding: 5px 4px 3px 4px;
                              text-align: left;
                           """)

buttons=[]

class FunkyButton(QtGui.QPushButton, animatedOpacity):
    def __init__(self, icon, text, scene,opacity=.3):
        QtGui.QPushButton.__init__(self,QtGui.QIcon(os.path.join(PATH,'icons',icon)),"")
        self.setAttribute(QtCore.Qt.WA_Hover, True)
        self.baseOpacity=opacity
        self.proxy=scene.addWidget(self)
        self.proxy.setOpacity(opacity)
        self.movingOp=False
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setMouseTracking(True)
        self.setStyleSheet("""
            QPushButton {
                background-color: lightgray;
                border: 3px solid darkgray;
                border-radius: 3px;
                padding: 5px 4px 3px 4px;
                min-width: 24px;
                min-height: 24px;
              }
            *:hover {
                border: 3px solid gray;
            }
            *:pressed {
                background-color: darkgray;
            }
        """)
        self.children=[]
        self.icon=icon
        self.text=text
        buttons.append(self)
        
class FunkyLineEdit(QtGui.QLineEdit, animatedOpacity):
    def __init__(self, scene,opacity=.3):
        QtGui.QLineEdit.__init__(self)
        self.baseOpacity=opacity
        self.proxy=scene.addWidget(self)
        self.proxy.setOpacity(opacity)
        self.movingOp=False
        self.setStyleSheet("""
            border: 1px solid gray;
            border-radius: 3px;
            padding: 5px 4px 3px 4px;
            min-width: 60px;
        """)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.children=[]

class FunkyFontList(QtGui.QFontComboBox, animatedOpacity):
    def __init__(self, scene,opacity=.3):
        QtGui.QFontComboBox.__init__(self)
        self.baseOpacity=opacity
        self.proxy=scene.addWidget(self)
        self.proxy.setOpacity(opacity)
        self.movingOp=False
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.children=[]
        self.setStyleSheet("""
            padding: 9px 0px 6px 3px;
        """)

class FunkyStatusBar(QtGui.QStatusBar, animatedOpacity):
    def __init__(self, scene,opacity=.3):
        QtGui.QStatusBar.__init__(self)
        self.baseOpacity=opacity
        self.proxy=scene.addWidget(self)
        self.proxy.setOpacity(opacity)
        self.movingOp=False
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.children=[]
        self.setStyleSheet("""
            border: 1px solid gray;
            border-radius: 3px;
            padding: 5px 4px 3px 4px;
            background-color: lightgray;
        """)
        self.setSizeGripEnabled(False)
         
class FunkyEditor(EditorClass, animatedOpacity):
    def __init__(self, parent):
        EditorClass.__init__(self, parent)
        self.setMouseTracking(True)
        self.viewport().setMouseTracking(True)
        self.defSize=self.font().pointSize()
        self.docName=''
        
        # This is a version that makes the editor be *in*
        # the graphicsview but things like selecting text fail
        
        #EditorClass.__init__(self)
        #self.setMouseTracking(True)
        #self.viewport().setMouseTracking(True)
        #self.defSize=self.font().pointSize()
        #self.docName=''
        #self.proxy=parent._scene.addWidget(self)
        #self.proxy.setOpacity(1)
        #self.movingOp=False
        #self.setFocusPolicy(QtCore.Qt.StrongFocus)
        #self.children=[]
        #self.parent=lambda: parent
        #self.proxy.setFlag(QtGui.QGraphicsItem.ItemIsMovable, False)

    def save(self):
        if not self.docName:
            self.saveas()
        else:
            f=codecs.open(self.docName,'w+','utf-8')
            f.truncate()
            f.write(unicode(self.toPlainText()))
            f.close()
            self.document().setModified(False)

    def saveas(self):
        fname=unicode(QtGui.QFileDialog.getSaveFileName())
        if fname:
            self.docName=fname
            self.save()

    def new(self):
        QtCore.QCoreApplication.instance().setOverrideCursor(QtCore.Qt.ArrowCursor)
        try:
            if self.document().isModified():
                r=QtGui.QMessageBox.question(None, "New Document - Marave", "The document \"%s\" has been modified."\
                    "\nDo you want to save your changes or discard them?"%self.docName or "UNNAMED",
                    QtGui.QMessageBox.Save|QtGui.QMessageBox.Discard|QtGui.QMessageBox.Cancel,QtGui.QMessageBox.Cancel)
                if r==QtGui.QMessageBox.Save:
                    self.save()
                elif r==QtGui.QMessageBox.Discard:
                    self.docName=''
                    self.setPlainText('')
            else:
                    self.docName=''
                    self.setPlainText('')
        except:
            pass
        QtCore.QCoreApplication.instance().restoreOverrideCursor()

    def open(self, fname=None):
        self.new()
        if self.docName:
            return
        if not fname:
            fname=unicode(QtGui.QFileDialog.getOpenFileName())
        if fname:
            self.docName=fname
            self.setPlainText(codecs.open(fname,'r','utf-8').read())

    def smaller(self):
        f=self.font()
        f.setPointSize(f.pointSize()-1)
        self.setFont(f)
        self.parent().settings.setValue('fontsize',self.font().pointSize())
        self.parent().settings.sync()
        
    def larger(self):
        f=self.font()
        f.setPointSize(f.pointSize()+1)
        self.setFont(f)
        self.parent().settings.setValue('fontsize',self.font().pointSize())
        self.parent().settings.sync()

    def default(self):
        f=self.font()
        f.setPointSize(self.defSize)
        self.setFont(f)
        self.parent().settings.setValue('fontsize',self.font().pointSize())
        self.parent().settings.sync()

    def mouseMoveEvent(self, ev):
        self.parent().showButtons()
        self.parent().showCursor()
        return QtGui.QPlainTextEdit.mouseMoveEvent(self, ev)

class MainWidget (QtGui.QGraphicsView):
    def __init__(self):
        QtGui.QGraphicsView.__init__(self)
        self.setStyleSheet("""
            border: 0px solid gray;
        """)
        self._scene=QtGui.QGraphicsScene()
        self._scene.changed.connect(self.scenechanged)
        self.setScene(self._scene)
        self.settings=QtCore.QSettings('NetManagers','Marave')
        self.changing=False
        self.visibleWidget=None

        # Used for margins and border sizes
        self.m=5
        
        # FIXME: self.minW should be a reasonable value based on text size 
        # or something.
        self.minW=100*self.m
        self.minH=80*self.m
        self.hasSize=False
        
        self.editor=None
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setMouseTracking(True)
        self.currentBG=None
        self.currentClick=None
        self.currentStation=None
        self.bgcolor=None
        self.bg=None
        self.bgItem=QtGui.QGraphicsPixmapItem()
        self._scene.addItem(self.bgItem)
        self.notifBar=FunkyStatusBar(self._scene, .7)
        self.notifBar.messageChanged.connect(self.notifChanged)
        self.beep=None
        self.music=None
        self.buttonStyle=0
        self.lang=None

        self.stations=[x.strip() for x in open(os.path.join(PATH,'radios.txt')).readlines()]

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        # These are the positions for the elements of the screen
        # They are recalculated on resize
        
        self.editorX=100
        self.editorY=40
        self.editorH=400
        self.editorW=400

        self.editor=FunkyEditor(self)
        self.editor.show()
        self.editor.setMouseTracking(True)
        self.editor.setFrameStyle(QtGui.QFrame.NoFrame)
        self.editor.setStyleSheet("""* {background-color: transparent;}
                                     QMenu {background-color: lightgray;
                                            border: 1px solid gray;
                                            }
                                  """)

        # Keyboard shortcuts
        self.sc1 = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+F"), self);
        self.sc1.activated.connect(self.showsearch)
        self.sc1b = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+R"), self);
        self.sc1b.activated.connect(self.showsearchreplace)

        # Taj mode!
        self.sc2 = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+T"), self);
        self.sc2.activated.connect(self.tajmode)

        ## Spell checker toggle
        #self.sc3 = QtGui.QShortcut(QtGui.QKeySequence("Shift+Ctrl+Y"), self);
        #self.sc3.activated.connect(self.togglespell)

        # Action shortcuts
        self.sc4 = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+O"), self);
        self.sc4.activated.connect(self.editor.open)
        self.sc5 = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+S"), self);
        self.sc5.activated.connect(self.editor.save)
        self.sc6 = QtGui.QShortcut(QtGui.QKeySequence("Shift+Ctrl+S"), self);
        self.sc6.activated.connect(self.editor.saveas)
        self.sc7 = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+N"), self);
        self.sc7.activated.connect(self.editor.new)
        self.sc8 = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Q"), self);

        # Prefs
        self.sc9 = QtGui.QShortcut(QtGui.QKeySequence("Shift+Ctrl+P"), self);
        self.sc9.activated.connect(self.showprefs)

        # Document information
        self.sc10 = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+I"), self);
        self.sc10.activated.connect(self.showinfo)

        self.editorBG=QtGui.QGraphicsRectItem()
        self.editorBG.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.editorBG.setCursor(QtCore.Qt.PointingHandCursor)
        self.editorBG.setBrush(QtGui.QColor(1,1,1))
        self._scene.addItem(self.editorBG)

        self.handles=[]
        
        for h in range(0,4):
            h=Handle(0,0,10,10)
            h.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
            h.setCursor(QtCore.Qt.SizeAllCursor)
            h.setOpacity(.5)
            h.setZValue(100)
            self._scene.addItem(h)
            self.handles.append(h)

        self.fontButton=FunkyButton("fonts.svg", 'Font', self._scene, 0)
        self.sizeButton=FunkyButton("size.svg", 'Size', self._scene, 0)
        self.fileButton=FunkyButton("file.svg", 'File', self._scene, 0)
        self.bgButton=FunkyButton("bg.svg", 'Bg', self._scene, 0)
        self.clickButton=FunkyButton("click.svg", 'Click', self._scene, 0)
        self.musicButton=FunkyButton("music.svg", 'Music', self._scene, 0)
        self.configButton=FunkyButton("configure.svg", 'Options', self._scene, 0)
        self.configButton.clicked.connect(self.showprefs)
        self.quitButton=FunkyButton("exit.svg", 'Quit', self._scene, 0)
        self.quitButton.clicked.connect(self.close)
        self.sc8.activated.connect(self.quitButton.animateClick)

        self.buttons=[self.fontButton, 
                      self.sizeButton, 
                      self.fileButton, 
                      self.bgButton, 
                      self.clickButton,
                      self.musicButton,
                      self.configButton,
                      self.quitButton,
                      ]


        self.fontList=FunkyFontList(self._scene,0)
        self.fontList.currentFontChanged.connect(self.changefont)
        self.fontColor=FunkyButton("color.svg", 'Color', self._scene,0)
        self.fontColor.clicked.connect(self.setfontcolor)
        self.fontButton.children+=[self.fontList,self.fontColor]

        self.size1=FunkyButton("minus.svg", 'Smaller', self._scene,0)
        self.size2=FunkyButton("equals.svg", 'Default', self._scene,0)
        self.size3=FunkyButton("plus.svg", 'Larger', self._scene,0)
        self.size1.clicked.connect(self.editor.smaller)
        self.size3.clicked.connect(self.editor.larger)
        self.size2.clicked.connect(self.editor.default)
        self.sizeButton.children+=[self.size1, self.size2, self.size3]


        self.file1=FunkyButton("open.svg", 'Open', self._scene, 0)
        self.file2=FunkyButton("save.svg", 'Save', self._scene, 0)
        self.file3=FunkyButton("saveas.svg", 'Save As', self._scene, 0)
        self.file1.clicked.connect(self.editor.open)
        self.file2.clicked.connect(self.editor.save)
        self.file3.clicked.connect(self.editor.saveas)
        self.fileButton.children+=[self.file1, self.file2, self.file3]

        self.bg1=FunkyButton("previous.svg", 'Previous', self._scene,0)
        self.bg2=FunkyButton("next.svg", 'Next', self._scene,0)
        self.bg3=FunkyButton("color.svg", 'Color', self._scene,0)
        self.bg1.clicked.connect(self.prevbg)
        self.bg2.clicked.connect(self.nextbg)
        self.bg3.clicked.connect(self.setbgcolor)
        self.bgButton.children+=[self.bg1, self.bg2, self.bg3]

        self.click1=FunkyButton("previous.svg", 'Previous', self._scene,0)
        self.click2=FunkyButton("next.svg", 'Next', self._scene,0)
        self.click3=FunkyButton("mute.svg", 'Mute', self._scene,0)
        self.click1.clicked.connect(self.prevclick)
        self.click2.clicked.connect(self.nextclick)
        self.click3.clicked.connect(self.noclick)
        self.clickButton.children+=[self.click1, self.click2, self.click3]
        
        self.music1=FunkyButton("previous.svg", 'Previous', self._scene,0)
        self.music2=FunkyButton("next.svg", 'Next', self._scene,0)
        self.music3=FunkyButton("mute.svg", 'Mute', self._scene,0)
        self.music1.clicked.connect(self.prevstation)
        self.music2.clicked.connect(self.nextstation)
        self.music3.clicked.connect(self.nostation)
        self.musicButton.children+=[self.music1, self.music2, self.music3]


        # Prefs widget
        self.prefsWidget=PrefsWidget(self._scene)
        self.prefsWidget.ui.close.clicked.connect(self.hidewidgets)
        self.prefsWidget.ui.saveTheme.clicked.connect(self.savetheme)
        self.prefsWidget.ui.themeList.currentIndexChanged.connect(self.loadtheme)
        self.prefsWidget.ui.buttonStyle.currentIndexChanged.connect(self.buttonstyle)
        self.prefsWidget.ui.langBox.currentIndexChanged.connect(self.setspellchecker)
        self.prefsWidget.ui.opacity.valueChanged.connect(self.editoropacity)
        self.prefsWidget.ui.buttonStyle.setCurrentIndex(self.settings.value('buttonstyle').toInt()[0])
        
        prefsLayout=QtGui.QGraphicsLinearLayout()
        prefsLayout.setContentsMargins(0,0,0,0)
        prefsLayout.addItem(self.prefsWidget.proxy)
        
        self.prefsBar=QtGui.QGraphicsWidget()
        self.prefsBar.setLayout(prefsLayout)
        self._scene.addItem(self.prefsBar)


        # Search widget
        self.searchWidget=SearchWidget(self._scene)
        self.searchWidget.ui.close.clicked.connect(self.hidewidgets)
        self.searchWidget.ui.next.clicked.connect(self.doFind)
        self.searchWidget.ui.previous.clicked.connect(self.doFindBackwards)
        
        searchLayout=QtGui.QGraphicsLinearLayout()
        searchLayout.setContentsMargins(0,0,0,0)
        searchLayout.addItem(self.searchWidget.proxy)
        
        self.searchBar=QtGui.QGraphicsWidget()
        self.searchBar.setLayout(searchLayout)
        self._scene.addItem(self.searchBar)

        # Search and replace widget
        self.searchReplaceWidget=SearchReplaceWidget(self._scene)
        self.searchReplaceWidget.ui.close.clicked.connect(self.hidewidgets)
        self.searchReplaceWidget.ui.next.clicked.connect(self.doFindR)
        self.searchReplaceWidget.ui.previous.clicked.connect(self.doFindRBackwards)
        self.searchReplaceWidget.ui.replace.clicked.connect(self.doReplace)
        #self.searchReplaceWidget.ui.replaceall.clicked.connect(self.doReplaceAll)
        
        searchReplaceLayout=QtGui.QGraphicsLinearLayout()
        searchReplaceLayout.setContentsMargins(0,0,0,0)
        searchReplaceLayout.addItem(self.searchReplaceWidget.proxy)
        
        self.searchReplaceBar=QtGui.QGraphicsWidget()
        self.searchReplaceBar.setLayout(searchReplaceLayout)
        self._scene.addItem(self.searchReplaceBar)
        
        # Event filters for showing/hiding buttons/cursor
        self.editor.installEventFilter(self)
        for b in self.buttons:
            b.installEventFilter(self)

        self.layoutButtons()
        self.loadprefs()

    def showinfo(self):
        txt=unicode(self.editor.toPlainText())
        lc=len(txt.splitlines())
        wc=len(re.split('\n\t ',txt))
        name=os.path.basename(self.editor.docName) or "UNNAMED"
        self.notify('Document: %s -- %d words %d lines %d characters.'%(
            name,wc,lc,len(txt) ))

    def notifChanged(self, msg):
        if unicode(msg):
            self.notifBar.targetOpacity=.7
        else:
            self.notifBar.targetOpacity=.0
        self.notifBar.moveOpacity()

    def notify(self, text):
        print 'NOTIF:',text
        self.notifBar.showMessage(text, 3000)
        self.notifBar.proxy.setPos(self.editorX, self.editorY+self.editorH+self.m)

    def layoutButtons(self):
        mainMenuLayout=QtGui.QGraphicsGridLayout()
        mainMenuLayout.setContentsMargins(0,0,0,0)
        for pos, button in enumerate(self.buttons):
            mainMenuLayout.addItem(button.proxy,pos,0)
        mainMenuLayout.setRowSpacing(len(self.buttons)-2,self.m*2)
        mainMenuLayout.addItem(self.fontList.proxy,0,2,1,2)
        mainMenuLayout.addItem(self.fontColor.proxy,0,1)
        mainMenuLayout.addItem(self.size1.proxy,1,1)
        mainMenuLayout.addItem(self.size2.proxy,1,2)
        mainMenuLayout.addItem(self.size3.proxy,1,3)
        mainMenuLayout.addItem(self.file1.proxy,2,1)
        mainMenuLayout.addItem(self.file2.proxy,2,2)
        mainMenuLayout.addItem(self.file3.proxy,2,3)
        mainMenuLayout.addItem(self.bg1.proxy,3,1)
        mainMenuLayout.addItem(self.bg2.proxy,3,2)
        mainMenuLayout.addItem(self.bg3.proxy,3,3)
        mainMenuLayout.addItem(self.click1.proxy,4,1)
        mainMenuLayout.addItem(self.click2.proxy,4,2)
        mainMenuLayout.addItem(self.click3.proxy,4,3)
        mainMenuLayout.addItem(self.music1.proxy,5,1)
        mainMenuLayout.addItem(self.music2.proxy,5,2)
        mainMenuLayout.addItem(self.music3.proxy,5,3)
        self.mainMenu=QtGui.QGraphicsWidget()
        self.mainMenu.setLayout(mainMenuLayout)
        self.mainMenu.setPos(self.editorX+self.editorW+20,self.editorY)
        self._scene.addItem(self.mainMenu)

    def editoropacity(self, v):
        self.notify("Setting opacity to: %s%%"%v)
        self.editorBG.setOpacity(v/100.)
        self.settings.setValue("editoropacity",v)
        self.settings.sync()

    def buttonstyle(self, idx):
        self.buttonStyle=idx
        self.settings.setValue('buttonstyle',self.buttonStyle)
        self.settings.sync()
        for b in buttons:
            if idx==0:
                b.setIcon(QtGui.QIcon(os.path.join(PATH,'icons',b.icon)))
                b.setText("")
                b.adjustSize()
            elif idx==1:
                b.setIcon(QtGui.QIcon())
                b.setText(b.text)
                b.adjustSize()
            elif idx==2:
                b.setIcon(QtGui.QIcon(os.path.join(PATH,'icons',b.icon)))
                b.setText(b.text)
                b.adjustSize()
        self.layoutButtons()

    def loadtheme(self, themeidx):
        if not themeidx:
            return
        themename=unicode(self.prefsWidget.ui.themeList.itemText(themeidx))
        themefile=os.path.join(PATH,'themes',themename)
        self.oldSettings=self.settings
        self.settings=QtCore.QSettings(themefile,QtCore.QSettings.IniFormat)
        self.loadprefs()
        self.settings=self.oldSettings
        self.saveprefs()
        
    def savetheme(self, themefile=None):
        if themefile is None or themefile is False:
            tdir=os.path.join(PATH,'themes')
            self.savetheme(QtGui.QFileDialog.getSaveFileName(None, "Marave - Save Theme",tdir))
            return
        self.oldSettings=self.settings
        self.settings=QtCore.QSettings(QtCore.QString(themefile),QtCore.QSettings.IniFormat)
        self.saveprefs()
        self.settings=self.oldSettings
        self.prefsWidget.loadthemelist()

    def saveprefs(self):
        # Save all settings at once
        self.settings.setValue('font',self.editor.font())
        self.settings.setValue('fontsize',self.editor.font().pointSize())
        self.settings.setValue('click',self.currentClick)
        self.settings.setValue('station',self.currentStation)
        if self.bgcolor:
            self.settings.setValue('bgcolor',self.bgcolor.name())
            self.settings.setValue('background',QtCore.QVariant())
        else:
            self.settings.setValue('bgcolor',QtCore.QVariant())
            self.settings.setValue('background',self.currentBG)

        if self.hasSize:
            self.settings.setValue('x',int(self.editorX))
            self.settings.setValue('y',int(self.editorY))
            self.settings.setValue('w',int(self.editorW))
            self.settings.setValue('h',int(self.editorH))

        self.settings.setValue('buttonstyle',self.buttonStyle)
        self.settings.setValue('editoropacity', self.editorBG.opacity()*100)

        self.settings.sync()

    def loadprefs(self):
        # Load all settings
        
        x=self.settings.value('x')
        y=self.settings.value('y')
        w=self.settings.value('w')
        h=self.settings.value('h')
        if x.isValid() and y.isValid() and w.isValid() and h.isValid():
            self.hasSize=True
            self.editorX=x.toInt()[0]
            self.editorY=y.toInt()[0]
            self.editorW=max(w.toInt()[0], self.minW)
            self.editorH=max(h.toInt()[0], self.minH)
        self.adjustPositions()
                
        f=QtGui.QFont()
        fname=self.settings.value('font')
        if fname.isValid():
            f.fromString(fname.toString())
        else:
            f.setFamily('courier')
        fs,ok=self.settings.value('fontsize').toInt()
        if ok:
            f.setPointSize(fs)
        self.editor.setFont(f)
        
        o,ok=self.settings.value('editoropacity').toInt()
        if ok:
            self.editorBG.setOpacity(o/100.)
        else:
            self.editorBG.setOpacity(.03)
        
        bs,ok=self.settings.value('buttonstyle').toInt()
        if ok:
            self.buttonStyle=bs
        else:
            self.buttonStyle=0
        self.buttonstyle(self.buttonStyle)
        
        c=self.settings.value('click')
        if c.isValid():
            self.setclick(unicode(c.toString()))
        else:
            self.noclick()
        
        s=self.settings.value('station')
        if s.isValid():
            self.setstation(unicode(s.toString()))
        else:
            self.nostation()

        bgcolor=self.settings.value('bgcolor')
        bg=self.settings.value('background')
        if not bg.isValid() and not bgcolor.isValid():
            # Probably first run
            self.nextbg()        
        elif bg.isValid():
            self.setbg(unicode(bg.toString()))
        elif bgcolor.isValid():
            self.setbgcolor(QtGui.QColor(bgcolor.toString()))

        l=self.settings.value('lang')
        if l.isValid():
            self.setspellchecker(unicode(l.toString()))
        else:
            self.setspellchecker('None')
            

    def setspellchecker(self, code):
        if isinstance (code, int):
            code=unicode(self.prefsWidget.ui.langBox.itemText(code))
        if "dict" not in self.editor.__dict__:
            # No pyenchant
            return
        if code == 'None':
            self.lang=None
            self.editor.killDict()
            self.prefsWidget.ui.langBox.setCurrentIndex(0)
        else:
            self.lang=code
            self.editor.initDict(self.lang)
            self.prefsWidget.ui.langBox.setCurrentIndex(self.prefsWidget.ui.langBox.findText(self.lang))
        self.settings.setValue('lang',self.lang)
        self.settings.sync()
        

    def close(self):
        QtCore.QCoreApplication.instance().setOverrideCursor(QtCore.Qt.ArrowCursor)
        if self.editor.document().isModified():
            r=QtGui.QMessageBox.question(None, "Close Document - Marave", "The document \"%s\" has been modified."\
                "\nDo you want to save your changes or discard them?"%self.editor.docName or "UNNAMED",
                QtGui.QMessageBox.Save|QtGui.QMessageBox.Discard|QtGui.QMessageBox.Cancel,QtGui.QMessageBox.Cancel)
            if r==QtGui.QMessageBox.Save:
                self.editor.save()
            elif r==QtGui.QMessageBox.Discard:
                self.saveprefs()
                QtGui.QGraphicsView.close(self)
                QtCore.QCoreApplication.instance().quit()
        else:
            self.saveprefs()
            QtGui.QGraphicsView.close(self)
            QtCore.QCoreApplication.instance().quit()
        QtCore.QCoreApplication.instance().restoreOverrideCursor()

    def showbar(self, w):
        self.hidewidgets()
        self.visibleWidget=w
        w.show()
        self.editor.resize(self.editorW, self.editorH-w.height())
        self.setFocus()
        w.targetOpacity=.7
        w.moveOpacity()

    def showsearchreplace(self):
        self.showbar(self.searchReplaceWidget)
        self.searchReplaceWidget.ui.text.setFocus()

    def showsearch(self):
        self.showbar(self.searchWidget)
        self.searchWidget.ui.text.setFocus()

    def showprefs(self):
        self.prefsWidget.ui.opacity.setValue(self.editorBG.opacity()*100)
        self.showbar(self.prefsWidget)


    def hidewidgets(self):
        for w in [self.searchWidget, self.searchReplaceWidget, self.prefsWidget]:            
            w.targetOpacity=.0
            w.moveOpacity()
            #w.hide()
        self.editor.setFocus()
        self.visibleWidget=None
        #self.editor.resize(self.editorW,self.editorH)

    def doReplaceAllBackwards(self):
        self.doReplaceAll(backwards=True)

    def doReplaceAll(self, backwards=False):
        pass

    def doReplaceBackwards (self):
        return self.doReplace(backwards=True)
        
    def doReplace(self, backwards=False):
        flags=QtGui.QTextDocument.FindFlags()
        if backwards:
            flags=QtGui.QTextDocument.FindBackward
        if self.searchWidget.ui.matchCase.isChecked():
            flags=flags|QtGui.QTextDocument.FindCaseSensitively

        text=unicode(self.searchWidget.ui.text.text())
        r=self.editor.find(text,flags)

    def doReplace(self):
        qc=self.editor.textCursor()
        if qc.hasSelection():
            qc.insertText(self.searchReplaceWidget.ui.replaceWith.text())
        self.doFindR(self.searchReplaceWidget.backwards)
            
    def doFindRBackwards (self):
        return self.doFindR(backwards=True)

    def doFindR(self, backwards=False):
        self.searchReplaceWidget.backwards=backwards
        flags=QtGui.QTextDocument.FindFlags()
        if backwards:
            flags=QtGui.QTextDocument.FindBackward
        if self.searchReplaceWidget.ui.matchCase.isChecked():
            flags=flags|QtGui.QTextDocument.FindCaseSensitively

        text=unicode(self.searchReplaceWidget.ui.text.text())
        r=self.editor.find(text,flags)

    def doFindBackwards (self):
        return self.doFind(backwards=True)

    def doFind(self, backwards=False):
        flags=QtGui.QTextDocument.FindFlags()
        if backwards:
            flags=QtGui.QTextDocument.FindBackward
        if self.searchWidget.ui.matchCase.isChecked():
            flags=flags|QtGui.QTextDocument.FindCaseSensitively

        text=unicode(self.searchWidget.ui.text.text())
        r=self.editor.find(text,flags)

    def setclick(self, clickname):
        self.currentClick=clickname
        self.notify('Switching click to: %s'%self.currentClick)
        self.beep = Phonon.createPlayer(Phonon.NotificationCategory,
                                  Phonon.MediaSource(os.path.join(PATH,'clicks',self.currentClick)))
        self.beep.play()
        self.settings.setValue('click',self.currentClick)
        self.settings.sync()

    def prevclick(self):
        clist=os.listdir(os.path.join(PATH,'clicks'))
        clist=[x for x in clist if not x.startswith('.')]
        clist.sort()
        try:
            idx=(clist.index(self.currentClick)-1)%len(clist)
        except ValueError:
            idx=-1
        self.setclick(clist[idx])

    def nextclick(self):
        clist=os.listdir(os.path.join(PATH,'clicks'))
        clist=[x for x in clist if not x.startswith('.')]
        clist.sort()
        try:
            idx=(clist.index(self.currentClick)+1)%len(clist)
        except ValueError:
            idx=-1
        self.setclick(clist[idx])

    def noclick(self):
        self.notify('Disabling click')
        self.beep=None

    def setstation(self, station):
        self.currentStation=station
        self.notify('switching music to: %s'%self.currentStation)
        self.music = Phonon.createPlayer(Phonon.MusicCategory,
                                  Phonon.MediaSource(self.currentStation))
        self.music.play()
        self.settings.setValue('station',self.currentStation)
        self.settings.sync()

    def prevstation(self):
        try:
            idx=(self.stations.index(self.currentStation)-1)%len(self.stations)
        except ValueError:
            idx=-1
        self.setstation(self.stations[idx])
        
    def nextstation(self):
        try:
            idx=(self.stations.index(self.currentStation)+1)%len(self.stations)
        except ValueError:
            idx=-1
        self.setstation(self.stations[idx])

    def nostation(self):
        if self.music:
            self.music.stop()
            self.notify('Disabling music')
    
    def setbg(self, bg):
        self.currentBG=bg
        self.bgcolor=None
        self.notify('Setting background to: %s'%self.currentBG)
        self.bg=QtGui.QImage(os.path.join(PATH,'backgrounds',bg))
        self.realBg=self.bg.scaled( self.size(), QtCore.Qt.KeepAspectRatioByExpanding)
        self.bgItem.setPixmap(QtGui.QPixmap(self.realBg))
        self.bgItem.setPos(self.width()-self.realBg.width(), self.height()-self.realBg.height())

    def prevbg(self):
        bglist=os.listdir(os.path.join(PATH,'backgrounds'))
        bglist=[x for x in bglist if not x.startswith('.')]
        bglist.sort()
        try:
            idx=(bglist.index(self.currentBG)-1)%len(bglist)
        except ValueError:
            idx=-1
        self.setbg(bglist[idx])
        
    def nextbg(self):
        bglist=os.listdir(os.path.join(PATH,'backgrounds'))
        bglist=[x for x in bglist if not x.startswith('.')]
        bglist.sort()
        try:
            idx=(bglist.index(self.currentBG)+1)%len(bglist)
        except ValueError:
            idx=0
        self.setbg(bglist[idx])
        
    def setbgcolor(self, bgcolor=None):
        if isinstance(bgcolor, QtGui.QColor):
            if bgcolor.isValid():
                self.bg=None
                self.realBG=None
                self.bgcolor=bgcolor
                pm=QtGui.QPixmap(self.width(), self.height())
                pm.fill(bgcolor)
                self.bgItem.setPixmap(pm)
                self.bgItem.setPos(0,0)
                self.notify('Setting background to: %s'%bgcolor.name())
        else:
            self.setbgcolor(QtGui.QColorDialog.getColor())

    def setfontcolor(self, color=None):
        if isinstance(color, QtGui.QColor):
            if color.isValid():
                self.editor.setStyleSheet("""background-color: transparent;
                                            color: %s;
                                          """%(unicode(color.name())))
        else:
            self.setfontcolor(QtGui.QColorDialog.getColor())

    def tajmode(self):
        self.noclick()
        self.nostation()
        self.setbgcolor(QtGui.QColor(0,0,0))
        self.setfontcolor(QtGui.QColor(0,255,0))
        
    def eventFilter(self, obj, event):
        if obj==self.editor:
            if event.type()==QtCore.QEvent.KeyPress:
                if self.beep:
                    self.beep.play()
                self.hideCursor()
                self.hideButtons()
            elif isinstance(event, QtGui.QMoveEvent):
                self.showButtons()
        elif isinstance(event, QtGui.QHoverEvent):
            for b in self.buttons:
                if b != obj:
                    b.hideChildren()
                else:
                    b.showChildren()
                self.showButtons()
        return QtGui.QGraphicsView.eventFilter(self, obj, event)

    def keyEvent(self, ev):
        self.hideCursor()
        QtGui.QGraphicsView.keyEvent(self, ev)

    def mouseMoveEvent(self, ev):
        self.showCursor()
        self.showButtons()
        QtGui.QGraphicsView.mouseMoveEvent(self, ev)

    def changefont(self, font):
        f=self.editor.font()
        f.setFamily(font.family())
        self.editor.setFont(f)
        self.settings.setValue('font',self.editor.font())
        self.settings.sync()

    def resizeEvent(self, ev):
        self._scene.setSceneRect(QtCore.QRectF(self.geometry()))
        if self.bg:
            self.setbg(self.currentBG)
        elif self.bgcolor:
            self.setbgcolor(self.bgcolor)
        if not self.hasSize:
            self.editorX=self.width()*.1
            self.editorH=max(self.height()*.9, self.minH)
            self.editorY=self.height()*.05
            self.editorW=max(self.width()*.6, self.minW)

        self.adjustPositions()
        
    def adjustPositions(self):
        m=self.m
        if self.editor:
            if self.visibleWidget:
                self.editor.setGeometry(self.editorX,self.editorY,self.editorW,self.editorH-self.visibleWidget.height()-self.m)
            else:
                self.editor.setGeometry(self.editorX,self.editorY,self.editorW,self.editorH)
            self.editorBG.setPos(self.editorX-m,self.editorY-m)
            self.editorBG.setBrush(QtGui.QColor(255,255,255,255))
            self.editorBG.setRect(0,0,self.editorW+2*m,self.editorH+2*m)
            self.mainMenu.setPos(self.editorX+self.editorW+3*m,self.editorY)
            self.searchBar.setPos(self.editorX,self.editorY+self.editorH-self.searchWidget.height())
            self.searchWidget.setFixedWidth(self.editor.width())
            self.searchReplaceBar.setPos(self.editorX,self.editorY+self.editorH-self.searchReplaceWidget.height())
            self.searchReplaceWidget.setFixedWidth(self.editor.width())
            self.prefsBar.setPos(self.editorX,self.editorY+self.editorH-self.prefsWidget.height())
            self.prefsWidget.setFixedWidth(self.editor.width())

            self.handles[0].setPos(self.editorX-2*m,self.editorY-2*m)
            self.handles[1].setPos(self.editorX+self.editorW,self.editorY-2*m)
            self.handles[2].setPos(self.editorX+self.editorW,self.editorY+self.editorH)
            self.handles[3].setPos(self.editorX-2*m,self.editorY+self.editorH)
            if self.hasSize:
                self.settings.setValue('x',int(self.editorX))
                self.settings.setValue('y',int(self.editorY))
                self.settings.setValue('w',int(self.editorW))
                self.settings.setValue('h',int(self.editorH))
                self.settings.sync()
            self.notifBar.proxy.setPos(self.editorX+m, self.editorY+self.editorH+2*m)
            self.notifBar.setFixedWidth(self.editorW-2*m)

    def scenechanged(self,region):
        if not self.changing:
            self.changing=True
            # See if the user dragged the editor
            flag=False
            m=self.m
            
            old=self.editorX, self.editorY, self.editorW, self.editorH
            
            # Editor dragged by the edge
            rect=self.editorBG.rect()
            pos=self.editorBG.pos()
            x=rect.x()+pos.x()
            y=rect.y()+pos.y()
            w=rect.width()
            h=rect.height()

            if x != self.editorX-m or   \
               y != self.editorY-m or   \
               w != self.editorW+2*m or \
               h != self.editorH+2*m:
                editorX=x+m
                editorY=y+m
                editorW=w-2*m
                editorH=h-2*m
                
                if editorW >= self.minW and editorH >= self.minH:
                    self.editorX = editorX
                    self.editorY = editorY
                    self.editorW = editorW
                    self.editorH = editorH
                self.hasSize=True
                self.adjustPositions()
                self.changing=False
                return
                   
            # Top-Left corner dragged
            rect=self.handles[0].rect()
            pos=self.handles[0].pos()
            x=rect.x()+pos.x()
            y=rect.y()+pos.y()
            if x != self.editorX-2*m or \
               y != self.editorY-2*m:
                    dx=x-self.editorX+2*m
                    dy=y-self.editorY+2*m
                    editorX=x+2*m
                    editorY=y+2*m
                    editorW=self.editorW-dx
                    editorH=self.editorH-dy
                    if editorW >= self.minW and editorH >= self.minH:
                        self.editorX = editorX
                        self.editorY = editorY
                        self.editorW = editorW
                        self.editorH = editorH                
                    self.hasSize=True
                    self.adjustPositions()
                    self.changing=False
                    return

            # Top-Right corner dragged
            rect=self.handles[1].rect()
            pos=self.handles[1].pos()
            x=rect.x()+pos.x()
            y=rect.y()+pos.y()
            if x != self.editorX+self.editorW or \
               y != self.editorY-2*m:
                    dx=x-self.editorX-self.editorW
                    dy=y-self.editorY+2*m
                    editorY=y+2*m
                    editorW=self.editorW+dx
                    editorH=self.editorH-dy
                    if editorW >= self.minW and editorH >= self.minH:
                        self.editorY = editorY
                        self.editorW = editorW
                        self.editorH = editorH                
                    self.hasSize=True
                    self.adjustPositions()
                    self.changing=False
                    return
                   
            # Bottom-Right corner dragged
            rect=self.handles[2].rect()
            pos=self.handles[2].pos()
            x=rect.x()+pos.x()
            y=rect.y()+pos.y()
            if x != self.editorX+self.editorW or \
               y != self.editorY+self.editorH:
                    dx=x-self.editorX-self.editorW
                    dy=y-self.editorY-self.editorH
                    editorW=self.editorW+dx
                    editorH=self.editorH+dy
                    if editorW >= self.minW and editorH >= self.minH:
                        self.editorW = editorW
                        self.editorH = editorH                
                    self.hasSize=True
                    self.adjustPositions()
                    self.changing=False
                    return

            # Bottom-Left corner dragged
            rect=self.handles[3].rect()
            pos=self.handles[3].pos()
            x=rect.x()+pos.x()
            y=rect.y()+pos.y()
            if x != self.editorX+2*m or \
               y != self.editorY+self.editorH:
                    dx=x-self.editorX+2*m
                    dy=y-self.editorY-self.editorH
                    editorX=x+2*m
                    editorW=self.editorW-dx
                    editorH=self.editorH+dy
                    if editorW >= self.minW and editorH >= self.minH:
                        self.editorX = editorX
                        self.editorW = editorW
                        self.editorH = editorH                
                    self.hasSize=True
                    self.adjustPositions()
                    self.changing=False
                    return

            self.changing=False
               
    def showButtons(self):
        for w in self.buttons + self.handles:
            w.targetOpacity=.8
            w.moveOpacity()

    def hideButtons(self):
        for w in self.buttons + self.handles:
            w.targetOpacity=0.
            w.moveOpacity()
            w.hideChildren()

    def hideCursor(self):
        QtCore.QCoreApplication.instance().setOverrideCursor(QtCore.Qt.BlankCursor)

    def showCursor(self):
        QtCore.QCoreApplication.instance().restoreOverrideCursor()

    def _show(self):
        self.showButtons()
        self.showFullScreen()
        self.show()
        self.raise_()
        self.activateWindow()
        self.adjustPositions()
        self.editor.setFocus()
        
def main():
    # Again, this is boilerplate, it's going to be the same on
    # almost every app you write
    app = QtGui.QApplication(sys.argv)
    print sys.argv

    if len(sys.argv) > 2:
        QtGui.QMessageBox.information(None,'FOCUS!','Marave only opens one document at a time.\nThe whole idea is focusing!\nSo, this is the first one you asked for.')

    window=MainWidget()
    if len(sys.argv) == 2:
        window.editor.open(sys.argv[1])
    window.show()
    window.raise_()
    window.activateWindow()
    QtCore.QTimer.singleShot(0,window._show)
    
    
    # It's exec_ because exec is a reserved word in Python
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
