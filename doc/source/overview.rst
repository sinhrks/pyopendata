.. ipython:: python
   :suppress:

   import pandas as pd
   pd.options.display.max_columns=10
   pd.options.display.max_rows=10

Overview
========

``pyopendata`` is a Python utility to offer an unified API to read world various data sources,
and output ``pandas.DataFrame``.

This is an unstable release and API is forced to be changed.

Installation
============

Use ``pip``.

.. code-block:: sh

    pip install pyopendata


Basic Usage
===========

This section explains how to retrieve data from website which uses CKAN API.

You can create ``DataStore`` instance to access CKAN website by passing CKAN URL to ``DataStore`` class.

.. ipython:: python

    import pyopendata as pyod

    store = pyod.DataStore('http://catalog.data.gov/')
    store

``DataStore.serch`` performs search by keyword. Results will be the list of packages. You can select a target package by slicing.

.. ipython:: python

    packages = store.search('department of health')
    packages

    packages[0]


Otherwise, specify the package name to be retrieved.

.. ipython:: python

    package = store.get('survey-summary')
    package

A package has resources (files) which contains actual data. You can use ``read`` method to read data as pandas ``DataFrame``.

.. important:: The target file must be the correct format which can be parsed by ``pandas`` IO functions.

.. ipython:: python

    package.resources[0]

    df = package.resources[0].read()
    df.head()

Or you can get raw data by specifying ``raw=True``.

.. ipython:: python

    raw = package.resources[0].read(raw=True)
    raw[:100]

Development
===========

https://github.com/sinhrks/pyopendata
