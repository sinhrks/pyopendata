# pylint: disable-msg=E1101,W0613,W0603

from __future__ import unicode_literals

import requests
import pandas


class DataSource(pandas.core.base.StringMixin):
    """
    Represents a data contained in the URL
    """

    _attrs = []

    def __init__(self, format=None, id=None, name=None, url=None, proxies=None,
                 size=None, **kwargs):

        if isinstance(format, pandas.compat.string_types):
            format = format.strip().upper()

        self.format = format
        self.id = id
        self.name = name
        self.url = self._normalize_url(url)
        self.proxies = proxies
        self.size = size

        for attr in self._attrs:
            value = kwargs.pop(attr, None)
            setattr(self, attr, value)

        self.kwargs = kwargs

    def __unicode__(self):
        return '{0} ({1})'.format(self.__class__.__name__, self.url)

    def _normalize_url(self, url):
        if url is None:
            return url
        elif url.endswith('/'):
            # remove final slash to handle sitename and filename commonly
            return url[:-1]
        else:
            return url

    def _requests_get(self, action='', params=None):
        """
        Internal requests.get to handle proxy
        """
        response = requests.get(self.url + action, params=params, proxies=self.proxies)
        return response

    def read(self, raw=False, **kwargs):
        """
        Read data from resource

        Parameters
        ----------
        raw : bool, default False
            If False, return pandas.DataFrame. If True, return raw data
        kwargs:
            Keywords passed to pandas.read_xxx function

        Returns
        -------
        data : pandas.DataFrame or requests.raw.data

        Notes
        -----
        - When the resource format is other than CSV, parsing pandas.DataFrame may fail.
          Use ``raw=True`` to get raw data in such cases.
        """
        if raw:
            return self._read_raw(**kwargs)
        else:
            return self._read(**kwargs)

    def _read(self):
        raise NotImplementedError

    def _read_raw(self, **kwargs):
        if self.url is None:
            raise ValueError('Unable to read raw data because URL is None')
        response = self._requests_get()
        return response.content


class RDFStore(DataSource):
    _connection_errors = (requests.exceptions.ConnectionError, ValueError)

    def get(self, name):
        raise NotImplementedError

    def search(self, serch_string):
        raise NotImplementedError

    @property
    def datasets(self):
        raise NotImplementedError
