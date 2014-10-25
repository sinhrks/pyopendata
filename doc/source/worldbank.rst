.. ipython:: python
   :suppress:

   import pandas as pd
   pd.options.display.max_columns=10
   pd.options.display.max_rows=10

Access to WorldBank Datasource
==============================

Create ``DataStore`` for WorldBank by passing ``worldbank`` at initialization.

.. ipython:: python

    import pyopendata as pyod

    store = pyod.DataStore('worldbank')
    store

Get `GDP per capita (current US$) <http://data.worldbank.org/indicator/NY.GDP.PCAP.CD>`_ data. The result will be a ``DataFrame`` which has ``DatetimeIndex`` as index, and indicator and conutries as column. The target URL is:

* http://data.worldbank.org/indicator/NY.GDP.PCAP.CD

We can read above URL as:

  * Resource ID: NY.GDP.PCAP.CD

.. ipython:: python

    resource = store.get('NY.GDP.PCAP.CD')
    resource

    df = resource.read();
    df.columns

You can access to specific data by slicing column.

.. ipython:: python

    jp = df['GDP per capita (current US$)']['Japan']
    jp
