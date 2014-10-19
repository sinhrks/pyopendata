.. ipython:: python
   :suppress:

   import pandas as pd
   pd.options.display.max_columns=10
   pd.options.display.max_rows=10

.. _overview.overview:

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

.. _overview.basic:

Basic Usage
===========

This section explains how to retrieve data from website which uses CKAN API.You can create ``DataStore`` instance to access CKAN website by passing CKAN URL to ``DataStore`` class.

In this example, we're going to retrieve the 'California Unemployment Statistics' data from `data.gov <https://www.data.gov/>_`. The target URL is:

* https://catalog.data.gov/dataset/california-unemployment-statistics/resource/ffd05307-4528-4d15-a370-c16222119227

We can read abov URL as:

  * CKAN API URL: https://catalog.data.gov/
  * Package ID: california-unemployment-statistics
  * Resource ID: ffd05307-4528-4d15-a370-c16222119227

.. ipython:: python

    import pyopendata as pyod

    store = pyod.DataStore('http://catalog.data.gov/')
    store

``DataStore.serch`` performs search by keyword. Results will be the list of packages. You can select a target package by slicing.

.. ipython:: python

    packages = store.search('Unemployment Statistics')
    packages

    packages[0]


Otherwise, specify the package name to be retrieved.

.. ipython:: python

    package = store.get('california-unemployment-statistics')
    package

A package has resources (files) which contains actual data. You use `get` method to retrieve the resource.

.. ipython:: python

    resource = package.get('ffd05307-4528-4d15-a370-c16222119227')
    resource

Once you get the resource, use ``read`` method to read data as pandas ``DataFrame``.

.. important:: The target file must be the correct format which can be parsed by ``pandas`` IO functions.

.. ipython:: python

    df = resource.read()
    df.head()

Or you can get raw data by specifying ``raw=True``.

.. ipython:: python

    raw = resource.read(raw=True)
    raw[:100]

