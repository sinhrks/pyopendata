.. ipython:: python
   :suppress:

   import pandas as pd
   pd.options.display.max_columns=10
   pd.options.display.max_rows=10

Access to Eurostat Datasource
=============================

Create ``DataStore`` for Eurostat by passing ``eurostat`` at initialization.

.. ipython:: python

    import pyopendata as pyod

    store = pyod.DataStore('eurostat')
    store

Get `Employed doctorate holders in non managerial and non professional occupations by fields of science <http://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=cdh_e_fos&lang=en>`_ data. The result will be a ``DataFrame`` which has ``DatetimeIndex`` as index and ``MultiIndex`` of attributes or countries as column. The target URL is:

* http://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=cdh_e_fos&lang=en

We can read above URL as:

  * Resource ID: cdh_e_fos

.. ipython:: python

    resource = store.get('cdh_e_fos')
    resource

    df = resource.read();
    df

You can access to specific data by slicing column.

.. ipython:: python

    usa = df['Percentage']['Total']['Natural sciences']['United States']
    usa

