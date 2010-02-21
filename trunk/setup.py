# -*- coding: utf-8 -*-

from distutils.cmd import Command
from distutils.core import setup
import os

class build_hl(Command):
    """Builds the syntax highlighter extension"""
    user_options = []
    description = "Build the syntax highlighter extension"
    
    def initialize_options(self):
        self._dir = os.path.abspath(os.path.dirname(__file__))

    def finalize_options(self):
        pass    
    
    def run(self):
        os.chdir(os.path.join(self._dir,'marave','highlight'))
        r=os.system('python configure.py')
        if r==0:
            os.system('make')
        os.chdir(self._dir)

setup(name='Marave',
      version='0.6',
      description='A relaxed text editor',
      author='Roberto Alsina',
      author_email='ralsina@netmanagers.com.ar',
      url='http://marave.googlecode.com',
      packages=['marave','marave.plugins'],
      scripts=['marave-script.py'],
      package_data={'marave': ['backgrounds/*',
                               'icons/*svg',
                               'clicks/*wav',
                               'themes/*',
                               'stylesheets/*',
                               'translations/*',
                               'highlight/*',
                               'radios.txt'
                               ]},
     cmdclass = { 'build_hl': build_hl },
     )
