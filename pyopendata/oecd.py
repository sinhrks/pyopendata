# pylint: disable-msg=E1101,W0613,W0603

from __future__ import unicode_literals

import numpy as np
import pandas as pd
from pandas.compat import iterkeys

from pyopendata.base import RDFStore, DataSource
from pyopendata.io import read_sdmx

class OECDStore(RDFStore):

    _url = 'http://stats.oecd.org/SDMX-JSON/data/'

    """
    Storage class to read OECD data
    """
    # http://www.oecd.org/about/membersandpartners/list-oecd-member-countries.htm
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

    def __init__(self, **kwargs):
        RDFStore.__init__(self, url=self._url, **kwargs)

        # cache
        self._datasets = None

    def __unicode__(self):
        return '{0} ({1})'.format(self.__class__.__name__, self.url)

    def is_valid(self):
        """
        Check whether the site has valid API.

        Returns
        -------
        is_valid : bool
        """
        return True

    @property
    def _target_countries(self):
        return '+'.join(list(iterkeys(self._countries)))

    def get(self, data_id):
        url = self.url + '/{0}/{1}/OECD?'.format(data_id, self._target_countries)
        return OECDResource(id=data_id, url=url)


class OECDResource(DataSource):

    def _read(self, **kwargs):
        data = self._requests_get().json()
        result = read_sdmx(data)
        return result
