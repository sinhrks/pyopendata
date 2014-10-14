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

* CKAN websites (www.data.gov, www.data.go.jp, etc)
* Eurostat
* OECD

Documentation
~~~~~~~~~~~~~

http://pyopendata.readthedocs.org/

Installation
~~~~~~~~~~~~

.. code-block:: sh

    pip install pyopendata

Basic Usage
~~~~~~~~~~~

This section explains how to retrieve data from website which uses CKAN API.You can create ``DataStore`` instance to access CKAN website by passing CKAN URL to ``DataStore`` class.

In this example, we're going to retrieve the 'California Unemployment Statistics' data from data.gov. The target URL is:

* https://catalog.data.gov/dataset/california-unemployment-statistics/resource/ffd05307-4528-4d15-a370-c16222119227

We can read abov URL as:

  * CKAN API URL: https://catalog.data.gov/dataset
  * Package ID: california-unemployment-statistics
  * Resource ID: ffd05307-4528-4d15-a370-c16222119227

.. code-block:: python

    >>> import pyopendata as pyod

    >>> store = pyod.DataStore('http://catalog.data.gov/')
    >>> store
    CKANStore (http://catalog.data.gov)

``DataStore.serch`` performs search by keyword. Results will be the list of packages. You can select a target package by slicing.

.. code-block:: python

    >>> packages = store.search('Unemployment Statistics')
    >>> packages
    [annual-survey-of-school-system-finances (1 resource),
     current-population-survey (1 resource),
     federal-aid-to-states (1 resource),
     current-population-survey-labor-force-statistics (2 resources),
     dataferrett (1 resource),
     mass-layoff-statistics (1 resource),
     unemployment-rate (3 resources),
     consolidated-federal-funds-report (1 resource),
     annual-survey-of-state-and-local-government-finances (1 resource),
     local-area-unemployment-statistics (2 resources)]

    >>> packages[0]
    annual-survey-of-school-system-finances (1 resource)


Otherwise, specify the package name to be retrieved.

.. code-block:: python

    >>> package = store.get('california-unemployment-statistics')
    >>> package
    Resource ID: ffd05307-4528-4d15-a370-c16222119227
    Resource Name: Comma Separated Values File
    Resource URL: https://data.lacity.org/api/views/5zrb-xqhf/rows.csv?accessType=DOWNLOAD
    Format: CSV, Size: None

A package has resources (files) which contains actual data. You use `get` method to retrieve the resource.

.. code-block:: python

    >>> resource = package.get('ffd05307-4528-4d15-a370-c16222119227')
    >>> resource

Once you get the resource, use ``read`` method to read data as pandas ``DataFrame``.

.. important:: The target file must be the correct format which can be parsed by ``pandas`` IO functions.

.. code-block:: python

    >>> df = resource.read()
    >>> df.head()
       Year Period                Area   Unemployment Rate  Labor Force  \
    0  2013    Jan          California               10.4%     18556500
    1  2013    Jan  Los Angeles County               10.9%      4891500
    2  2013    Jan    Los Angeles City                 12%      1915600
    3  2013    Feb          California  9.699999999999999%     18648300
    4  2013    Feb  Los Angeles County               10.3%      4924000

       Employment  Unemployment Adjusted Preliminary
    0    16631900       1924600  Not Adj  Not Prelim
    1     4357800        533800  Not Adj  Not Prelim
    2     1684800        230800  Not Adj  Not Prelim
    3    16835900       1812400  Not Adj  Not Prelim
    4     4418000        506000  Not Adj  Not Prelim


Or you can get raw data by specifying ``raw=True``.

.. code-block:: python

    >>> raw = resource.read(raw=True)
    >>> raw[:100]
    'Year,Period,Area,Unemployment Rate,Labor Force,Employment,Unemployment,Adjusted,Preliminary\n2013,Jan'



