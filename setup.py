#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='pyopendata',
      version='0.0.1',
      description='Python utility to get open data from CKAN, Eurostat and OECD websites',
      author='sinhrks',
      author_email='sinhrks@gmail.com',
      url='http://pyopendata.readthedocs.org',
      license = 'BSD',
      packages=find_packages(),
      package_data={'pyopendata.io': ['tests/data/jsdmx/*.json',
                                      'tests/data/jstat/*.json',
                                      'tests/data/sdmx/*.json']},
      install_requires=open('requirements.txt').read().splitlines())
