# -*- coding: utf-8 -*-

import os

PATH = os.path.abspath(os.path.dirname(__file__))

class Plugin (object):
    pass

def initPlugins():
    l=[]
    for p in os.listdir(PATH):
        if p.endswith('.py') and p != 'plugins.py':
            l.append(p)
    for p in l:
        __import__(p[:-3], None, None, '')

def listPLugins():
    return Plugin.__subclasses__()