.. ipython:: python
   :suppress:

   import pandas as pd
   pd.options.display.max_columns=10
   pd.options.display.max_rows=10

Access to OECD Datasource
=========================

Create ``DataStore`` for OECD by passing ``oecd`` at initialization.

.. ipython:: python

    import pyopendata as pyod

    store = pyod.DataStore('oecd')
    store

Get `Trade Union Density <http://stats.oecd.org/Index.aspx?DataSetCode=UN_DEN>`_ data. The result will be a ``DataFrame`` which has ``DatetimeIndex`` as index and conutries as column.

.. ipython:: python

    resource = store.get('UN_DEN')
    resource

    df = resource.read()
    df

You can access to specific data by slicing column.

.. ipython:: python

    usa = df['United States']
    usa
