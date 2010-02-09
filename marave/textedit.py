# -*- coding: utf-8 -*-

from PyQt4 import QtGui

class TextEdit (QtGui.QPlainTextEdit):
    
    def contextMenuEvent(self, event):
        popup_menu = self.createStandardContextMenu()
        pal=QtGui.QApplication.instance().palette()
        popup_menu.setStyleSheet("""
                                  * { background-color: %s;
                                      color: %s;}
                                  """%(unicode(pal.color(QtGui.QPalette.Button).name()),
                                        unicode(pal.color(QtGui.QPalette.WindowText).name())))
        popup_menu.exec_(event.globalPos())
