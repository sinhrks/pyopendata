.. ipython:: python
   :suppress:

   import pandas as pd
   pd.options.display.max_columns=10
   pd.options.display.max_rows=10

Access to CKAN Datasource
=========================

``DataStore`` supports an access to CKAN API. Websites which has CKAN API are listed in the following URL.

http://ckan.org/instances/

Initialize CKAN Datasource
--------------------------

To create ``DataStore`` for CKAN access, pass URL offers API. For example, `data.gov <http://www.data.gov>`_ offers API via:

http://catalog.data.gov/api

In this case, any of following 4 URL formats can be used for ``DataStore`` initialization.

 * http://catalog.data.gov/api
 * http://catalog.data.gov/api/
 * http://catalog.data.gov
 * http://catalog.data.gov/

.. ipython:: python

    import pyopendata as pyod

    pyod.DataStore('http://catalog.data.gov/api')
    pyod.DataStore('http://catalog.data.gov/api/')
    pyod.DataStore('http://catalog.data.gov')
    pyod.DataStore('http://catalog.data.gov/')

.. important:: `DateStore` validates the input URL using CKAN `site_read` function. If this function is closed on the target website, initialization should fail. In this case, instantiate ``pyod.CKANStore`` directly.

For example, `data.go.jp <http://www.data.go.jp>`_ doesn't allow to use `site_read`.

.. ipython:: python

    # should fail
    pyod.DataStore('http://www.data.go.jp/data')

    # should be OK
    pyod.CKANStore('http://www.data.go.jp/data')


Read Data
---------

Once you create ``DataStore``, you can access to data as described in :ref:`Basic Usage<overview.basic>`.
