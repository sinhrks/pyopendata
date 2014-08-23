# pylint: disable-msg=E1101,W0613,W0603

import pandas


class RDFStore(pandas.core.base.StringMixin):
    _attrs = []

    def __init__(self, format=None, id=None, name=None, url=None,
                 size=None, **kwargs):
        self.format = format
        self.id = id
        self.name = name
        self.url = self._normalize_url(url)
        self.size = size

        for attr in self._attrs:
            value = kwargs.get(attr, None)
            setattr(self, attr, value)

    def _normalize_url(self, url):
        if url is None:
            return url
        elif url.endswith('/'):
            # remove final slash to handle sitename and filename commonly
            return url[:-1]
        else:
            return url

