# pylint: disable-msg=E1101,W0613,W0603

import pandas
import numpy as np
from pandas.compat import u, range, iterkeys, iteritems

from pyopendata.base import RDFStore, DataSource

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

    def _get_values_from_dict(self, d, required_num):
        """
        Parse OECD returned json format
        """
        values = []
        for i in range(required_num):
            try:
                value = d[str(i)][0]
            except KeyError:
                value = np.nan
            values.append(value)
        return values

    def _read(self, **kwargs):
        data = self._requests_get().json()
        # create index and column
        structure = data['structure']
        index = structure['dimensions']['observation'][0]['values']
        columns = structure['dimensions']['series'][0]['values']

        # Currently supports yearly data only
        index = [int(i['name']) for i in index]
        columns = [c['name'] for c in columns]

        dataset = data['dataSets']
        # assert len(dataset) == 1
        dataset = dataset[0]
        series = dataset['series']

        df_data = {}
        for k, v in iteritems(series):
            # each observation contains time-series data (index-wise data)
            obs = v['observations']
            values = self._get_values_from_dict(obs, len(index))
            df_data_key = columns[int(k)]
            df_data[df_data_key] = values
        return pandas.DataFrame(df_data, columns=columns, index=index)

