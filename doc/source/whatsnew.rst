.. ipython:: python
   :suppress:

   import pandas as pd
   pd.options.display.max_columns=10
   pd.options.display.max_rows=10

What's New
==========

0.0.2
-----

- Support WorldBank API by `DataStore('worldbank')`.
- `DataResource` now has `get` method to search a resource in the package.
- `DataResource` now caches data once read from data source.
- `EuroStatStore` and `EuroStatResource` renamed to `EurostatStore` and `EurostatResource`.


0.0.1
-----

Initial Release