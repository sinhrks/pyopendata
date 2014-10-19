# pylint: disable-msg=E1101,W0613,W0603

from __future__ import unicode_literals
from __future__ import division

import os
import sys

import requests
import pandas
from pandas.compat import StringIO, bytes_to_str, binary_type
from pandas.util.decorators import Appender

from pyopendata.util import network

_shared_docs = dict()
_base_doc_kwargs = dict(resource_klass='DataResource')


class DataResource(pandas.core.base.StringMixin):
    """
    Represents a data contained in the URL
    """

    # url being used as default / static
    _url = None
    # kwargs which should be stored as instance properties
    _attrs = []
    # instance properties used as cache (overwritten by inherited classes)
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
        # cache for raw content
        self._raw_content = None

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

    _shared_docs['read'] = (
        """Read data from resource

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
        - Depending on the target format, parsing to ``pandas.DataFrame`` may fail.
          Use ``raw=True`` to get raw data in such cases.
        """)

    @Appender(_shared_docs['read'])
    def read(self, raw=False, **kwargs):
        if raw:
            content = self._read_raw(**kwargs)
            return content.getvalue()
        else:
            return self._read(**kwargs)

    def _read(self):
        raise NotImplementedError

    def _read_raw(self, **kwargs):
        if self._raw_content is None:
            response = self._requests_get()
            content_length = response.headers.get('content-length')
            out = StringIO()

            try:
                content_length = int(content_length)
                pb = network.ProgressBar(total=content_length)

                for chunk in response.iter_content(self._chunk_size):
                    if chunk:
                        out.write(chunk)
                        pb.update(self._chunk_size)
                self._raw_content = out
            except Exception as e:
                # print(e)
                # no content_length or any errors
                if isinstance(response.content, binary_type):
                    out.write(bytes_to_str(response.content))
                else:
                    out.write(response.content)
                self._raw_content = out
        return self._raw_content


class DataStore(DataResource):
    _connection_errors = (requests.exceptions.ConnectionError, ValueError)
    _cache_attrs = ['_datasets']

    def __new__(cls, kind_or_url=None, proxies=None):
        from pyopendata.ckan import CKANStore
        from pyopendata.eurostat import EurostatStore
        from pyopendata.oecd import OECDStore
        from pyopendata.undata import UNdataStore
        from pyopendata.worldbank import WorldBankStore

        if kind_or_url == 'oecd' or cls is OECDStore:
            return OECDStore._initialize(proxies=proxies)
        elif kind_or_url == 'eurostat' or cls is EurostatStore:
            return EurostatStore._initialize(proxies=proxies)
        elif kind_or_url == 'undata' or cls is UNdataStore:
            return UNdataStore._initialize(proxies=proxies)
        elif kind_or_url == 'worldbank' or cls is WorldBankStore:
            return WorldBankStore._initialize(proxies=proxies)

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

    _shared_docs['is_valid'] = (
        """Check whether the site has valid API.

        Returns
        -------
        is_valid : bool
        """)

    @Appender(_shared_docs['is_valid'])
    def is_valid(self):
        return True

    _shared_docs['get'] = (
        """Get resource by resource_id.

        Parameters
        ----------
        resource_id : str
            id to specify resource

        Returns
        -------
        result : %(resource_klass)s
        """)

    @Appender(_shared_docs['get'] % _base_doc_kwargs)
    def get(self, name):
        raise NotImplementedError

    _shared_docs['search'] = (
        """Search resources by search_string.

        Parameters
        ----------
        search storing : str
            keyword to search

        Returns
        -------
        result : list of %(resource_klass)s
        """)

    @Appender(_shared_docs['search'] % _base_doc_kwargs)
    def search(self, serch_string):
        raise NotImplementedError

    @property
    def datasets(self):
        raise NotImplementedError
