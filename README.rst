pyopendata
==========

.. image:: https://pypip.in/version/pyopendata/badge.svg
    :target: https://pypi.python.org/pypi/pyopendata/
    :alt: Latest Version

.. image:: https://readthedocs.org/projects/pyopendata/badge/?version=latest
    :target: http://pyopendata.readthedocs.org/en/latest/
    :alt: Latest Docs

.. image:: https://travis-ci.org/sinhrks/pyopendata.svg?branch=master
    :target: https://travis-ci.org/sinhrks/pyopendata

Overview
~~~~~~~~

``pyopendata`` is a Python utility to offer an unified API to read world various data sources,
and output ``pandas.DataFrame``. Which covers:
- CKAN websites (www.data.gov, www.data.go.jp, etc)
- Eurostat
- OECD

Documentation
~~~~~~~~~~~~~

http://pyopendata.readthedocs.org/

Installation
~~~~~~~~~~~~

.. code-block:: sh

    pip install pyopendata

Usage
~~~~~

.. code-block:: python

    >>> import pyopendata as pyod

    # You can create datastore for access by passing URL.
    >>> store = pyod.DataStore('http://catalog.data.gov/')
    >>> store
    CKANStore (http://catalog.data.gov)

    # Get package specifying name.
    >>> package = store.get('survey-summary')
    >>> package
    survey-summary (4 resources)

    # Dataset contains resources which contains actual data
    >>> package.resources[0]
    Resource ID: 56969e54-244f-4022-b2f4-6f648bc749f5
    Resource Name: Comma Separated Values File
    Resource URL: https://data.medicare.gov/api/views/tbry-pc2d/rows.csv?accessType=DOWNLOAD
    Format: CSV, Size: None

    # Call read method to get data as pandas DataFrame format.
    >>> package.resources[0].read()
                                                    Location  Processing Date
    0      701 MONROE STREET NW\nRUSSELLVILLE, AL 35653\n...       08/01/2014
    1      701 MONROE STREET NW\nRUSSELLVILLE, AL 35653\n...       08/01/2014
    2      701 MONROE STREET NW\nRUSSELLVILLE, AL 35653\n...       08/01/2014

    [46484 rows x 47 columns]

    # Or can get raw data by passing raw keyword
    >>> package.resources[0].read(raw=True)
    Federal Provider Number,Provider Name, ....
    015009,"BURNS NURSING HOME, INC." ...

