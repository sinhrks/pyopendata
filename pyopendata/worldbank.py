# pylint: disable-msg=E1101,W0613,W0603

from __future__ import unicode_literals

import copy
import datetime
import json
import warnings

import numpy as np
import pandas as pd
from pandas.compat import StringIO, iterkeys, iteritems
from pandas.util.decorators import Appender

from pyopendata.base import DataStore, DataResource, _shared_docs
from pyopendata.io import read_jsdmx
from pyopendata.util import network


_worldbank_doc_kwargs = dict(resource_klass='WorldBankResource')


class WorldBankStore(DataStore):
    """
    Storage class to read World Bank data
    """
    # http://search.worldbank.org/api/v2/projects

    _url = 'http://api.worldbank.org'
    _cache_attrs = ['_datasets']

    @Appender(_shared_docs['get'] % _worldbank_doc_kwargs)
    def get(self, resource_id):
        query = '/countries/all/indicators/{0}?format=json'.format(resource_id)
        url = self.url + query
        return WorldBankResource(id=resource_id, url=url)


class WorldBankResource(DataResource):

    entries_per_page = 500

    def _read_pagenate(self, **kwargs):
        """Because of pagenation, raw_contet stores parsed json data as it is
        * _read_raw will return it after converting to string
        * _read will convert it to pandas.DataFrame
        """
        if self._raw_content is None:
            page = 1
            contents = []
            pb = None

            while(True):
                query = '&page={0}&per_page={1}'.format(page, self.entries_per_page)
                data = self._requests_get(query).json()
                meta = data[0]
                content = data[1]

                if pb is None:
                    # progressbar cannot be initialized
                    # arter retrieving total number of pages
                    pb = network.ProgressBar(total=meta['pages'])
                pb.update(1)
                contents.extend(content)
                if page >= meta['pages']:
                    break
                page = page + 1

            self._raw_content = contents
        return self._raw_content

    def _read_raw(self, **kwargs):
        contents = copy.deepcopy(self._read_pagenate(**kwargs))
        return StringIO(json.dumps(contents))

    def _read(self, **kwargs):
        # meta, data = json.loads(json_raw)
        page = 1
        contents = []

        def assign_value(entry):
            # each attribute can contain dict as value.
            # In this case, retrieve 'value' from the list
            #
            # {'date': '2009',
            #  'country': {'id': 'L5', 'value': 'Andean Region'},
            #  'indicator': {'id': 'NY.GDP.PCAP.KD.ZG', 'value': 'GDP per capita growth (annual %)'},
            #  'decimal': '1', 'value': None},

            for k, v in iteritems(entry):
                if isinstance(v, dict):
                    entry[k] = v['value']
            if 'date' in entry:
                dt = entry['date']
                if '1900' <= dt <= '2100':
                    entry['date'] = datetime.datetime(int(dt), 1, 1)
            for key in ['decimal', 'value']:
                if key in entry and entry[key] is not None:
                    entry[key] = float(entry[key])
            if entry['decimal'] != 0:
                message = "The entry has 'decimal' != 0, it may not be parsed properly "
                warnings.warn(message , UserWarning)
            return entry
        contents = copy.deepcopy(self._read_pagenate(**kwargs))
        contents = [assign_value(c) for c in contents]
        result = pd.DataFrame(contents)

        try:
            result = pd.pivot_table(result, index='date', columns=['indicator', 'country'],
                                    values='value', aggfunc=np.sum)
        except Exception:
            pass

        return result



