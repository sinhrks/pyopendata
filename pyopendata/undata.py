# pylint: disable-msg=E1101,W0613,W0603

from __future__ import unicode_literals

import pandas as pd
import numpy as np
from pandas.compat import u, bytes_to_str, range, iterkeys, iteritems

from pyopendata.base import DataStore, DataResource
import pyopendata.io.sdmx as sdmx



class UNdataStore(DataStore):
    """
    Storage class to read UNdata data
    """

    _url = 'http://data.un.org/Handlers'
    _cache_attrs = ['_datasets']

    # reference
    # http://blog.overcognition.com/?p=422

    def is_valid(self):
        """
        Check whether the site has valid API.

        Returns
        -------
        is_valid : bool
        """
        return True

    def get(self, data_id):
        resource = UNdataResource(id=data_id)
        return resource

    @property
    def datasets(self):
        if self._datasets is None:
            response = self._requests_get('/ExplorerHandler.ashx?t=marts')
            # format is json, but `Nodes` is not double-quoted
            # Thus, unable to parse by response.json()

            # replace 1st Nodes to "Nodes"
            content = bytes_to_str(response.content)
            content = content.replace(str('Nodes'), str('"Nodes"'), 1)
            import json
            result = json.loads(content)
            nodes = result['Nodes']

            # import html.parser
            # import HTMLParser
            # parser = HTMLParser.HTMLParser()
            def delabel(node):
                # print(node['label'])
                # print(parser.feed(node['label']))
                return node

            nodes = [delabel(n) for n in nodes]
            datasets = pd.DataFrame(result['Nodes'])

            self._datasets = []
            # for dataflow in root.iter(sdmx._STRUCTURE + 'Dataflow'):
            #     name = sdmx._get_english_name(dataflow)
            #     id = dataflow.get('id')
            #     resource = EurostatResource(name=name, id=id)
            #     self._datasets.append(resource)
        return self._datasets


class UNdataResource(DataResource):

    def __init__(self, **kwargs):
        DataResource.__init__(self, **kwargs)
        # query = 'DataMartId={0}&DataFilter={1}&Format=csv'.format(self.mart, self.code)

        self.url = UNdataStore._url + '/DocumentDownloadHandler.ashx?t=bin&id={0}'.format(self.id)

        # not sure which API is better
        # DownloadHandler.ashx?DataMartId=Comtrade&DataFilter=_l1Code%3a1&Format=csv
        # DocumentDownloadHandler.ashx?t=bin&id=164

    def _read(self, skiprows=[0, 1, 2, 3], **kwargs):
        try:
            data = self._read_raw()
            result = pd.read_excel(data, skiprows=skiprows, **kwargs)
        except Exception:
            result = pd.read_excel(self.url, skiprows=skiprows, **kwargs)
        return result


