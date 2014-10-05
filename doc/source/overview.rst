.. ipython:: python
   :suppress:

   import pandas as pd
   pd.options.display.max_columns=10
   pd.options.display.max_rows=10

Overview
========

``pyopendata`` is an Python utility to offer an unified API to world various data sources, outputs ``pandas.DataFrame`` format.

This is an unstable release and APIs are forced to be changed.

Installation
============

Use ``pip``.

.. code-block:: sh

   pip install pyopendata


Basic Usage
===========

This section explains how to retrieve data from website which uses CKAN API.

You can create instance for access by passing CKAN URL to DataStore class.

.. ipython:: python

    import pyopendata as pyod

    store = pyod.DataStore('http://catalog.data.gov/')
    store

Perform search by keywords. Results will be the list of datasets. You can select a target by slicing.

.. ipython:: python

    packages = store.search('department of health')
    packages

    packages[0]


Otherwise, specify the name to be retrieved.

.. ipython:: python

    package = store.get('survey-summary')
    package

A package contains resources which has actual data. You can use ``read`` method to get data as pandas ``DataFrame``.

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
