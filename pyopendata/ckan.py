# pylint: disable-msg=E1101,W0613,W0603

import requests

import pandas
from pandas.compat import u

from pyopendata.base import RDFStore

class CKANStore(RDFStore):
    """
    Base class to read RDF

    Parameters
    ----------
    url : string
        URI for CKAN API

    """
    def __init__(self, url, **kwargs):
        RDFStore.__init__(self, url=url, **kwargs)

        if self.url.endswith('api'):
            # remove '/api'
            self.url = self.url[:-4]

        # cache
        self._packages = None
        self._groups = None
        self._tags = None

    def __unicode__(self):
        return '{0} ({1})'.format(self.__class__.__name__, self.url)

    def is_valid(self):
        """
        Check whether the site has valid API.

        Returns
        -------
        is_valid : bool
        """
        try:
            response = requests.get('{0}/api/action/site_read'.format(self.url))
            results = self._validate_response(response)
            return True
        except (requests.exceptions.ConnectionError, ValueError):
            return False

    def get(self, object_id):
        # get smaller object to larger object (resource -> package)
        try:
            return self.get_resource(object_id)
        except (requests.exceptions.ConnectionError, ValueError):
            pass
        try:
            return self.get_package(object_id)
        except (requests.exceptions.ConnectionError, ValueError):
            raise

    def get_package(self, package_id):
        params = dict(id=package_id)
        response = requests.get('{0}/api/action/package_show'.format(self.url), params=params)
        results = self._validate_response(response)
        return CKANPackage(**results)

    def get_resource(self, resource_id):
        params = dict(id=resource_id)
        response = requests.get('{0}/api/action/resource_show'.format(self.url), params=params)
        results = self._validate_response(response)
        return CKANResource(**results)

    def get_resources_from_tag(self, tag):
        params = dict(id=tag)
        response = requests.get('{0}/api/action/tag_show'.format(self.url), params=params)
        results = self._validate_response(response)
        results = results['packages']
        return [CKANResource(**r) for r in results]

    def get_packages_from_group(self, group_id):
        params = dict(id=group_id)
        response = requests.get('{0}/api/action/group_show'.format(self.url), params=params)
        results = self._validate_response(response)
        results = results['packages']
        return [CKANPackage(**r) for r in results]

    def search(self, search_string):
        # get smaller object to larger object (resource -> package)
        try:
            return self.search_resource(search_string)
        except (requests.exceptions.ConnectionError, ValueError):
            pass
        try:
            return self.search_package(search_string)
        except (requests.exceptions.ConnectionError, ValueError):
            raise

    def search_package(self, search_string):
        params = dict(q=search_string)
        response = requests.get('{0}/api/action/package_search'.format(self.url), params=params)
        results = self._validate_response(response)
        results = results['results']
        return [CKANPackage(**r) for r in results]

    def search_resource(self, search_string):
        # different params from search_packages
        # params = dict(query=search_string)
        # response = requests.get('{0}/api/action/resource_search'.format(self.url), params=params)

        # avoid escape search string (:)
        request_url = '{0}/api/action/resource_search?query={1}'
        response = requests.get(request_url.format(self.url, search_string))
        results = self._validate_response(response)
        results = results['results']
        return [CKANResource(**r) for r in results]

    @property
    def packages(self):
        if self._packages is None:
            response = requests.get('{0}/api/action/package_list'.format(self.url))
            results = self._validate_response(response)
            if isinstance(results, list):
                self._packages = results
            elif isinstance(results, dict):
                # internally calls ``current_package_list_with_resources``?
                results = results['results']
                self._packages = [CKANPackage(**r) for r in results]
            else:
                raise ValueError(type(results), results)
        return self._packages

    @property
    def groups(self):
        if self._groups is None:
            response = requests.get('{0}/api/action/group_list'.format(self.url))
            self._groups = self._validate_response(response)
        return self._groups

    @property
    def tags(self):
        if self._tags is None:
            response = requests.get('{0}/api/action/tag_list'.format(self.url))
            self._tags= self._validate_response(response)
        return self._tags

    def _validate_response(self, response):
        if response.status_code != 200:
            raise ValueError(response.status_code)

        response_dict = response.json()
        if response_dict['success'] is not True:
            raise valueError(responce_dict['message'])
        return response_dict['result']


class CKANPackage(RDFStore):

    def __init__(self, resources=None, **kwargs):
        RDFStore.__init__(self, **kwargs)

        if isinstance(resources, list):
            self.resources = [CKANResource(**r) for r in resources]
        else:
            raise ValueError(type(resources), resources)

    def __unicode__(self):
        source_len = len(self.resources)
        if source_len == 0:
            return '{0} (Empty)'.format(self.name)
        elif source_len == 1:
            return '{0} (1 resource)'.format(self.name)
        else:
            return '{0} ({1} resources)'.format(self.name, source_len)

    def read(self, **kwargs):
        source_len = len(self.resources)
        if source_len == 0:
            return pandas.DataFrame()
        elif source_len == 1:
            return self.resources[0].read(**kwargs)
        else:
            raise ValueError('Package has {0} resources. Use CKANResource.read()'.format(source_len))


class CKANResource(RDFStore):
    _attrs = ['size_text']
    _supported_formats = ('CSV', 'JSON', 'XLS')

    def __init__(self, resources=None, **kwargs):
        RDFStore.__init__(self, **kwargs)

        if resources is None:
            self.resources = None
        elif isinstance(resources, list):
            self.resources = [CKANResource(**r) for r in resources]
        else:
            raise ValueError(type(resources), resources)

    def __unicode__(self):
        rep_str = u("""Resource ID: {id}
Resource Name: {name}
Resource URL: {url}
Format: {format}, Size: {size}""").format(id=self.id, name=self.name,
                                         url=self.url,
                                         format=self.format,
                                         size=self.size_text)
        return rep_str

    def read(self, raw=False, **kwargs):
        """
        Read data from resource

        Parameters
        ----------
        raw : bool, default False
            If False, return pandas.DataFrame. If True, return raw data

        Returns
        -------
        data : pandas.DataFrame or requests.raw.data
        """
        if raw:
            return self._read_raw(**kwargs)

        if self.resources is None:
            return self._read(**kwargs)
        else:
            source_len = len(self.resources)
            if source_len == 0:
                return pandas.DataFrame()
            elif source_len == 1:
                return self.resources[0].read(**kwargs)
            else:
                raise ValueError('Package has {0} resources. Use CKANResource.read()'.format(source_len))

    def _read(self, **kwargs):
        if self.url is None:
            raise ValueError('Unable to read data because url is None')
        if self.format in ('CSV', 'CSV/TXT'):
            return pandas.read_csv(self.url, **kwargs)
        elif self.format == 'XLS':
            return pandas.read_excel(self.url, **kwargs)
        elif self.format == 'JSON':
            return pandas.read_json(self.url, **kwargs)
        elif self.format == 'N/A':
            raise ValueError('{0} is not available on the store'.format(self.name))
        else:
            raise ValueError('Unsupported read format: {0}'.format(self.format))