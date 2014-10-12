# pylint: disable-msg=E1101,W0613,W0603

from __future__ import unicode_literals

import numpy as np
import pandas as pd
from pandas.compat import iterkeys
from pandas.util.decorators import Appender

from pyopendata.base import DataStore, DataResource, _shared_docs
from pyopendata.io import read_jsdmx


_oecd_doc_kwargs = dict(resource_klass='OECDResource')


class OECDStore(DataStore):
    """
    Storage class to read OECD data
    """
    # http://www.oecd.org/about/membersandpartners/list-oecd-member-countries.htm

    _url = 'http://stats.oecd.org/SDMX-JSON/data'
    _cache_attrs = ['_datasets']

    _countries = {'AUS': 'AUSTRALIA',
                  'AUT': 'AUSTRIA',
                  'BEL': 'BELGIUM',
                  'CAN': 'CANADA',
                  'CHL': 'CHILE',
                  'CZE': 'CZECH REPUBLIC',
                  'DNK': 'DENMARK',
                  'EST': 'ESTONIA',
                  'FIN': 'FINLAND',
                  'FRA': 'FRANCE',
                  'DEU': 'GERMANY',
                  'GRC': 'GREECE',
                  'HUN': 'HUNGARY',
                  'ISL': 'ICELAND',
                  'IRL': 'IRELAND',
                  'ISR': 'ISRAEL',
                  'ITA': 'ITALY',
                  'JPN': 'JAPAN',
                  'KOR': 'KOREA',
                  'LUX': 'LUXEMBOURG',
                  'MEX': 'MEXICO',
                  'NLD': 'NETHERLANDS',
                  'NZL': 'NEW ZEALAND',
                  'NOR': 'NORWAY',
                  'POL': 'POLAND',
                  'PRT': 'PORTUGAL',
                  'SVK': 'SLOVAK REPUBLIC',
                  'SVN': 'SLOVENIA',
                  'ESP': 'SPAIN',
                  'SWE': 'SWEDEN',
                  'CHE': 'SWITZERLAND',
                  'TUR': 'TURKEY',
                  'GBR': 'UNITED KINGDOM',
                  'USA': 'UNITED STATES',
                  'OECD': 'OECD'}

    # def __init__(self, **kwargs):
    #     DataStore.__init__(self, url=self._url, **kwargs)

    @property
    def _target_countries(self):
        return '+'.join(list(iterkeys(self._countries)))

    @Appender(_shared_docs['get'] % _oecd_doc_kwargs)
    def get(self, resource_id):
        url = self.url + '/{0}/{1}/OECD?'.format(resource_id, self._target_countries)
        return OECDResource(id=resource_id, url=url)


class OECDResource(DataResource):

    def _read(self, **kwargs):
        data = self._requests_get().json()
        result = read_jsdmx(data)
        # There is data not be sorted by time
        result = result.sort_index()
        return result
