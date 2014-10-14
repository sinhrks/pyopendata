# pylint: disable-msg=E1101,W0613,W0603

from __future__ import unicode_literals

import numpy as np
import pandas as pd
from pandas.compat import u, range, iterkeys, iteritems
from pandas.util.decorators import Appender

from pyopendata.base import DataStore, DataResource, _shared_docs
import pyopendata.io.sdmx as sdmx


_eurostat_doc_kwargs = dict(resource_klass='EurostatResource')


class EurostatStore(DataStore):
    """
    Storage class to read Eurostat data
    """
    # http://epp.eurostat.ec.europa.eu/portal/page/portal/sdmx_web_services/getting_started/rest_sdmx_2.1

    _url = 'http://www.ec.europa.eu/eurostat/SDMX/diss-web/rest'
    _cache_attrs = ['_datasets']

    @Appender(_shared_docs['get'] % _eurostat_doc_kwargs)
    def get(self, data_id):
        resource = EurostatResource(id=data_id)
        return resource

    @property
    def datasets(self):
        if self._datasets is None:
            response = self._requests_get('/dataflow/ESTAT/all/latest')
            import xml.etree.cElementTree as ET
            root = ET.fromstring(response.content)

            self._datasets = []
            for dataflow in root.iter(sdmx._STRUCTURE + 'Dataflow'):
                name = sdmx._get_english_name(dataflow)
                id = dataflow.get('id')
                resource = EurostatResource(name=name, id=id)
                self._datasets.append(resource)
        return self._datasets


class EurostatResource(DataResource):

    def __init__(self, **kwargs):
        DataResource.__init__(self, **kwargs)
        self.url = EurostatStore._url + '/data/{0}/?'.format(self.id)
        self.dsd_url = EurostatStore._url + '/datastructure/ESTAT/DSD_{0}'.format(self.id)

        self._dsd = None

    @property
    def dsd(self):
        if self._dsd is None:
            dsd = self._requests_get(url=self.dsd_url).content
            self._dsd = sdmx._read_sdmx_dsd(dsd)
        return self._dsd

    def _read(self, **kwargs):

        try:
            # try to use dsd if available
            dsd = self.dsd
        except Exception:
            dsd = None

        data = self._requests_get().content
        result = sdmx.read_sdmx(data, dsd=dsd)
        # There is data not sorted by time
        result = result.sort_index()
        return result


