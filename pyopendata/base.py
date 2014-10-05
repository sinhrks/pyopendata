# pylint: disable-msg=E1101,W0613,W0603

from __future__ import unicode_literals
from __future__ import division

import sys

import requests
import pandas
from pandas.compat import StringIO, bytes_to_str, binary_type

class DataResource(pandas.core.base.StringMixin):
    """
    Represents a data contained in the URL
    """

    # url being used as default / static
    _url = None
    # kwargs which should be stored as instance properties
    _attrs = []
    # instance properties used as cache
    _cache_attrs = []

    _chunk_size = 1024 * 1024

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

        self._initialize_attrs(self)

        self.kwargs = kwargs

    def __unicode__(self):
        return '{0} ({1})'.format(self.__class__.__name__, self.url)

    @classmethod
    def _initialize_attrs(cls, obj):
        """
        Initialize object with class attributes
        """
        # initialize cache attrs
        for attr in cls._cache_attrs:
            setattr(obj, attr, None)
        return obj

    @classmethod
    def _normalize_url(cls, url):
        if url is None:
            return cls._url
        elif url.endswith('/'):
            # remove final slash to handle sitename and filename commonly
            return url[:-1]
        else:
            return url

    def _requests_get(self, action='',  params=None, url=None):
        """
        Internal requests.get to handle proxy
        """
        if url is None:
            url = self.url
        response = requests.get(url + action, params=params, proxies=self.proxies)
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
            content = self._read_raw(**kwargs)
            return content.getvalue()
        else:
            return self._read(**kwargs)

    def _read(self):
        raise NotImplementedError

    def _read_raw(self, **kwargs):
        response = self._requests_get()
        content_length = response.headers.get('content-length')
        out = StringIO()

        try:
            content_length = int(content_length)
            downloaded = 0
            pb_len      # progress bar's number of characters

            for chunk in response.iter_content(self._chunk_size):
                if chunk:
                    out.write(chunk)
                    downloaded += self._chunk_size
                    done = max(int(pb_len * downloaded / content_length), pb_len)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (pb_len - done)) )
                    sys.stdout.flush()
            return out
        except Exception:
            # no content_length or any errors
            if isinstance(response.content, binary_type):
                out.write(bytes_to_str(response.content))
            else:
                out.write(response.content)
            return out


class DataStore(DataResource):
    _connection_errors = (requests.exceptions.ConnectionError, ValueError)
    _cache_attrs = ['_datasets']

    def __new__(cls, kind_or_url=None, proxies=None):
        from pyopendata.oecd import OECDStore
        from pyopendata.eurostat import EuroStatStore
        from pyopendata.ckan import CKANStore

        if kind_or_url == 'oecd' or cls is OECDStore:
            return OECDStore._initialize(proxies=proxies)
        elif kind_or_url == 'eurostat' or cls is EuroStatStore:
            return EuroStatStore._initialize(proxies=proxies)

        elif cls is CKANStore:
            # skip validation if initialized with CKANStore directly
            store = CKANStore._initialize(url=kind_or_url, proxies=proxies)
            return store
        else:
            store = CKANStore._initialize(url=kind_or_url, proxies=proxies)
            if store.is_valid():
                return store
        raise ValueError('Unable to initialize DataStore with {0}'.format(kind_or_url))

    def __init__(self, kid_or_url=None, proxies=None):
        # handle with __new__
        pass

    @classmethod
    def _initialize(cls, url=None, proxies=None):
        obj = object.__new__(cls)
        obj.url = cls._normalize_url(url)
        obj.proxies = proxies
        obj = cls._initialize_attrs(obj)
        return obj

    def get(self, name):
        raise NotImplementedError

    def search(self, serch_string):
        raise NotImplementedError

    @property
    def datasets(self):
        raise NotImplementedError
