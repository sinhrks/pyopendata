#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='pyopendata',
      version='0.0.1',
      description='Python utility to get open data from websites',
      author='sinhrks',
      author_email='sinhrks@gmail.com',
      url='https://github.com/sinhrks/pyopendata',
      license = 'BSD',
      packages=find_packages(),
      package_data={'pyopendata.io': ['tests/data/jsdmx/*.json',
                                      'tests/data/jstat/*.json',
                                      'tests/data/sdmx/*.json']},
      install_requires = ['setuptools',
                         'pandas>=0.14.0',
                         'requests',
                         'xlrd'])
