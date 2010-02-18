# -*- coding: utf-8 -*-

import os
from PyQt4 import QtGui

PATH = os.path.abspath(os.path.dirname(__file__))

class Plugin (object):
    @classmethod
    def selectorWidget(self):
        w=QtGui.QWidget()
        w.check=QtGui.QCheckBox(self.description)
        w.conf=QtGui.QPushButton(QtGui.QIcon(os.path.join(PATH,'..','icons','configure.svg')),'')
        l=QtGui.QHBoxLayout()
        l.addWidget(w.check)
        l.addWidget(w.conf)
        w.setLayout(l)
        return w

def initPlugins():
    l=[]
    for p in os.listdir(PATH):
        if p.endswith('.py') and p != 'plugins.py':
            l.append(p)
    for p in l:
        __import__('plugins.'+p[:-3], level=-1)

def listPlugins():
    return Plugin.__subclasses__()