# -*- coding: utf-8 -*-
import sys

from PyQt4 import QtCore, QtGui
from SyntaxHighlighter import srchiliteqt


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    w = QtGui.QPlainTextEdit()
    w.show()

    hp=srchiliteqt.Qt4SyntaxHighlighter(w.document())
    hp.init('python.lang')

    if len(sys.argv) >1:
        w.setPlainText(open(sys.argv[1]).read())

    sys.exit(app.exec_())