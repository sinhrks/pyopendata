# pylint: disable-msg=E1101,W0613,W0603

from __future__ import unicode_literals

import pandas
import numpy as np
from pandas.compat import u, range, iterkeys, iteritems

from pyopendata.base import RDFStore

class EuroStatStore(RDFStore):

    _url = 'http://www.ec.europa.eu/eurostat/SDMX/diss-web/rest/'

    """
    Storage class to read Eurostat data
    """
    # http://epp.eurostat.ec.europa.eu/portal/page/portal/sdmx_web_services/getting_started/rest_sdmx_2.1
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

    def get(self, data_id):
        raise NotImplementedError

    @property
    def datasets(self):
        response = self._requests_get('/dataflow/ESTAT/all/latest')
        import xml.etree.ElementTree as ET
        root = ET.fromstring(response.content)
        structure = '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}'

        result = []
        for dataflow in root.iter(structure + 'Dataflow'):
            result.append(dataflow)
        return result



