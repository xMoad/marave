# -*- coding: utf-8 -*-

from plugins import Plugin

class Smarty(Plugin):
    shortcut='Ctrl+\''
    description='Smart quote and dash replacement'

    def run(self):
        print "my client window is:", self.client