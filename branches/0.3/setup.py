# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name='Marave',
      version='0.3',
      description='A relaxed text editor',
      author='Roberto Alsina',
      author_email='ralsina@netmanagers.com.ar',
      url='http://marave.googlecode.com',
      packages=['marave'],
      scripts=['marave/marave'],
      package_data={'marave': ['backgrounds/*jpg',
                               'icons/*svg',
                               'clicks/*wav',
                               'themes/*',
                               'themes/*',
                               'stylesheets/*',
                               'radios.txt'
                               ]},
     )
