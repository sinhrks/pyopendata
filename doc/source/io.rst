.. ipython:: python
   :suppress:

   import pandas as pd
   pd.options.display.max_columns=10
   pd.options.display.max_rows=10

IO Methods
==========

``io`` module has some methods to parse specific types of XMML/JSON.

    * :ref:`read_jstat<io.read_jstat>`
    * :ref:`read_sdmx<io.read_sdmx>`
    * :ref:`read_jsdmx<io.read_jsdmx>`

.. _io.read_jstat:

read_jstat
----------

Read `JSON-stat <http://json-stat.org/>`_ file.

.. ipython:: python

    import pyopendata as pyod
    pyod.io.read_jstat('http://json-stat.org/samples/us-gsp.json')

.. _io.read_sdmx:

read_sdmx
---------

Read `SDMX-XML <http://epp.eurostat.ec.europa.eu/portal/page/portal/sdmx_web_services/getting_started/rest_sdmx_2.1>`_ file. The format is used in Eurostat.

.. _io.read_jsdmx:

read_jsdmx
----------

Read `SDMX-JSON <http://stats.oecd.org/opendataapi/Json.htm>`_ file. The format is used in OECD.

