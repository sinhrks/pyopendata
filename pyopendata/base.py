# pylint: disable-msg=E1101,W0613,W0603

import requests

import pandas


class RDFStore(pandas.core.base.StringMixin):
    _attrs = []

    def __init__(self, format=None, id=None, name=None, url=None,
                 size=None, **kwargs):

        if isinstance(format, pandas.compat.string_types):
            format = format.strip().upper()

        self.format = format
        self.id = id
        self.name = name
        self.url = self._normalize_url(url)
        self.size = size

        for attr in self._attrs:
            value = kwargs.pop(attr, None)
            setattr(self, attr, value)

        self.kwargs = kwargs

    def get(self, name):
        raise NotImplementedError

    def search(self, serch_string):
        raise NotImplementedError

    def _normalize_url(self, url):
        if url is None:
            return url
        elif url.endswith('/'):
            # remove final slash to handle sitename and filename commonly
            return url[:-1]
        else:
            return url

    def _read_raw(self, **kwargs):
        if self.url is None:
            raise ValueError('Unable to read raw data because URL is None')
        response = requests.get(self.url)
        return response.content

