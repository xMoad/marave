# -*- coding: utf-8 -*-

import os
from PyQt4 import QtGui

PATH = os.path.abspath(os.path.dirname(__file__))

class Plugin (object):
    
    instances = {}
    
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
        
    @classmethod
    def instance(self,pluginClass):
        if pluginClass not in self.instances:
            self.instances[pluginClass]=pluginClass()
        return self.instances[pluginClass]
            

    @classmethod
    def initPlugins(self):
        l=[]
        for p in os.listdir(PATH):
            if p.endswith('.py') and p != 'plugins.py':
                l.append(p)
        for p in l:
            __import__('plugins.'+p[:-3], level=-1)

    @classmethod
    def listPlugins(self):
        return Plugin.__subclasses__()