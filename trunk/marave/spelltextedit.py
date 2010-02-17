#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
__license__ = 'MIT'
__copyright__ = '2009, John Schember <john@nachtimwald.com>'
__docformat__ = 'restructuredtext en'
 
import re
import sys
import os
import codecs

# Spell checker support
try:
    import enchant
except ImportError:
    enchant = None

# Syntax highlight support
try:
    from highlight.SyntaxHighlighter import srchiliteqt
except ImportError:
    srchiliteqt = None


from PyQt4.Qt import QAction
from PyQt4.Qt import QApplication
from PyQt4.Qt import QEvent
from PyQt4.Qt import QMenu
from PyQt4.Qt import QMouseEvent
from PyQt4.Qt import QPlainTextEdit
from PyQt4.Qt import QSyntaxHighlighter
from PyQt4.Qt import QTextCharFormat
from PyQt4.Qt import QTextCursor
from PyQt4.Qt import Qt
from PyQt4.Qt import QColor
from PyQt4.Qt import QPalette
from PyQt4.QtCore import pyqtSignal
from PyQt4 import QtGui, QtCore
 
class SpellTextEdit(QPlainTextEdit):

    langChanged = QtCore.pyqtSignal(QtCore.QString)
    
    def __init__(self, *args):
        QPlainTextEdit.__init__(self, *args)
        self.docName = None
        self.initDict()

    def initDict(self, lang=None):
        if not enchant:
            return
        # Default dictionary based on the current locale.
        if lang==None:
            try:
                self.dict = enchant.Dict()
            except enchant.DictNotFoundError:
                self.dict=None
        else:
            self.dict = enchant.Dict(lang)
        self.highlighter = SpellHighlighter(self.document())
        if self.dict:
            self.highlighter.setDict(self.dict)
            self.highlighter.rehighlight()

    def killDict(self):
        print 'Disabling spellchecker'
        self.highlighter.setDocument(None)
        self.dict=None

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            # Rewrite the mouse event to a left button event so the cursor is
            # moved to the location of the pointer.
            event = QMouseEvent(QEvent.MouseButtonPress, event.pos(),
                Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
        QPlainTextEdit.mousePressEvent(self, event)
 
    def contextMenuEvent(self, event):
        popup_menu = self.createStandardContextMenu()
        pal=QApplication.instance().palette()
        # This fixes Issue 20
        popup_menu.setStyleSheet("""
                                  * { background-color: %s;
                                      color: %s;}
                                  """%(unicode(pal.color(QPalette.Button).name()),
                                        unicode(pal.color(QPalette.WindowText).name())))
 
        # Select the word under the cursor.
        cursor = self.textCursor()
        cursor.select(QTextCursor.WordUnderCursor)
        self.setTextCursor(cursor)
 
        # Check if the selected word is misspelled and offer spelling
        # suggestions if it is.
        if enchant:
            if self.textCursor().hasSelection():
                text = unicode(self.textCursor().selectedText())
                if not self.dict.check(text):
                    spell_menu = QMenu(self.tr('Spelling Suggestions'))
                    for word in self.dict.suggest(text):
                        action = SpellAction(word, spell_menu)
                        action.correct.connect(self.correctWord)
                        spell_menu.addAction(action)
                    # Only add the spelling suggests to the menu if there are
                    # suggestions.
                    if len(spell_menu.actions()) != 0:
                        popup_menu.insertSeparator(popup_menu.actions()[0])
                        popup_menu.insertMenu(popup_menu.actions()[0], spell_menu)
                        
        # FIXME: add change dict and disable spellcheck options
 
        popup_menu.exec_(event.globalPos())
 
    def correctWord(self, word):
        '''
        Replaces the selected text with word.
        '''
        cursor = self.textCursor()
        cursor.beginEditBlock()
 
        cursor.removeSelectedText()
        cursor.insertText(word)
 
        cursor.endEditBlock()

    def save(self):
        if not self.docName:
            self.saveas()
        else:
            try:
                f=codecs.open(self.docName,'w+','utf-8')
                f.truncate()
                f.write(unicode(self.toPlainText()))
                f.close()
                self.document().setModified(False)
                self.parent().notify(self.tr('Document saved'))
            except:
                QtGui.QMessageBox.information(self.parent(), "Error - Marave",
                "Error saving %s."%self.docName)
                

    def saveas(self):
        QtCore.QCoreApplication.instance().setOverrideCursor(QtCore.Qt.ArrowCursor)
        fname=unicode(QtGui.QFileDialog.getSaveFileName(self.parent()))
        QtCore.QCoreApplication.instance().restoreOverrideCursor()
        if fname:
            self.docName=fname
            self.save()

    def new(self):
        QtCore.QCoreApplication.instance().setOverrideCursor(QtCore.Qt.ArrowCursor)
        try:
            if self.document().isModified():
                r=QtGui.QMessageBox.question(self.parent(), "New Document - Marave", "The document \"%s\" has been modified."\
                    "\nDo you want to save your changes or discard them?"%self.docName or "UNNAMED",
                    QtGui.QMessageBox.Save|QtGui.QMessageBox.Discard|QtGui.QMessageBox.Cancel,QtGui.QMessageBox.Cancel)
                if r==QtGui.QMessageBox.Save:
                    self.save()
                elif r==QtGui.QMessageBox.Discard:
                    self.docName=''
                    self.setPlainText('')
                    self.parent().setWindowFilePath('Untitled')
            else:
                    self.docName=''
                    self.setPlainText('')
                    self.parent().setWindowFilePath('Untitled')
        except:
            pass
        QtCore.QCoreApplication.instance().restoreOverrideCursor()

    def open(self, fname=None):
        self.new()
        if self.docName:
            return
        if not fname:
            QtCore.QCoreApplication.instance().setOverrideCursor(QtCore.Qt.ArrowCursor)
            fname=unicode(QtGui.QFileDialog.getOpenFileName(self.parent()))
            QtCore.QCoreApplication.instance().restoreOverrideCursor()
        if fname:
            self.docName=fname
            
                            
            if os.path.exists(fname):
                if os.path.isfile(fname):
                    # If spell checking is disabled, use syntax highlighter
                    if not self.dict and srchiliteqt:
                        self.highlighter=srchiliteqt.Qt4SyntaxHighlighter(self.document())
                        self.highlighter.setDefaultToMonosapce(False)
                        langName=self.highlighter.getLangDefFileFromFileName(fname)
                        self.langChanged.emit(langName)
                        self.highlighter.init(langName)
                    text=codecs.open(fname,'r','utf-8').read()
                    self.setPlainText(text)
                        
                else:
                    QtGui.QMessageBox.information(self.parent(), "Error - Marave",
                    "%s is not a file."%fname)
            
        self.parent().setWindowFilePath(self.docName)

    def setHL(self, lang, style):
        """Disable spellchecking and enable syntax highlighting"""
        
        if isinstance(self.highlighter, SpellHighlighter):
            self.killDict()
            self.highlighter=srchiliteqt.Qt4SyntaxHighlighter(self.document())
            self.highlighter.setDefaultToMonosapce(False)
        self.highlighter.setDocument(self.document())
        self.highlighter.init(lang)
        self.highlighter.setFormattingStyle(style)
        t=self.document().toPlainText()
        self.setPlainText(t)

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
 
 
class SpellHighlighter(QSyntaxHighlighter):
 
    WORDS = u'(?iu)[\w\']+'
 
    def __init__(self, *args):
        QSyntaxHighlighter.__init__(self, *args)
 
        self.dict = None
 
    def setDict(self, dict):
        self.dict = dict
 
    def highlightBlock(self, text):
        if not self.dict:
            return
 
        text = unicode(text)
 
        format = QTextCharFormat()
        #format.setUnderlineColor(Qt.red)
        format.setUnderlineStyle(QTextCharFormat.DotLine)
 
        for word_object in re.finditer(self.WORDS, text):
            if not self.dict.check(word_object.group()):
                self.setFormat(word_object.start(),
                    word_object.end() - word_object.start(), format)
 
 
class SpellAction(QAction):
 
    '''
    A special QAction that returns the text in a signal.
    '''
 
    correct = pyqtSignal(unicode)
 
    def __init__(self, *args):
        QAction.__init__(self, *args)
 
        self.triggered.connect(lambda x: self.correct.emit(
            unicode(self.text())))
 
 
def main(args=sys.argv):
    app = QApplication(args)
 
    spellEdit = SpellTextEdit()
    spellEdit.show()
 
    return app.exec_()
 
if __name__ == '__main__':
    sys.exit(main())
