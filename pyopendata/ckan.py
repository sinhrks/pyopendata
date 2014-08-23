# pylint: disable-msg=E1101,W0613,W0603

import urllib2
import urllib
import json

import pandas
from pandas.compat import u

from pyopendata.base import RDFStore

class CKANStore(RDFStore):
    """
    Base class to read RDF

    Parameters
    ----------
    path : string
        URI for CKAN

    """
    def __init__(self, url, **kwargs):
        RDFStore.__init__(self, url=url, **kwargs)

        # cache
        self._packages = None
        self._groups = None
        self._tags = None

    def get_package_from_id(self, package_id):
        data = urllib.urlencode(dict(id=package_id))
        request = urllib2.Request('{0}/api/action/package_show?{1}'.format(self.url, data))
        response = urllib2.urlopen(request)
        results = self._validate_response(response)
        return CKANPackage(**results)

    def get_resources_from_tag(self, tag):
        data = urllib.urlencode(dict(id=tag))
        request = urllib2.Request('{0}/api/action/tag_show?{1}'.format(self.url, data))
        response = urllib2.urlopen(request)
        results = self._validate_response(response)
        results = results['packages']

        return [CKANResource(**r) for r in results]

    def get_packages_from_group(self, group_id):
        data = urllib.urlencode(dict(id=group_id))
        request = urllib2.Request('{0}/api/action/group_show?{1}'.format(self.url, data))
        response = urllib2.urlopen(request)
        results = self._validate_response(response)
        results = results['packages']
        return [CKANPackage(**r) for r in results]

    @property
    def packages(self):
        if self._packages is None:
            request = urllib2.Request('{0}/api/action/package_list'.format(self.url))
            response = urllib2.urlopen(request)
            results = self._validate_response(response)
            if isinstance(results, list):
                self._packages = results
            elif isinstance(results, dict):
                results = results['results']
                self._packages = [CKANPackage(**r) for r in results]
            else:
                raise ValueError(type(results), results)
        return self._packages

    @property
    def groups(self):
        if self._groups is None:
            request = urllib2.Request('{0}/api/action/group_list'.format(self.url))
            response = urllib2.urlopen(request)
            self._groups = self._validate_response(response)
        return self._groups

    @property
    def tags(self):
        if self._tags is None:
            request = urllib2.Request('{0}/api/action/tag_list'.format(self.url))
            response = urllib2.urlopen(request)
            self._tags= self._validate_response(response)
        return self._tags

    def _validate_response(self, response):
        if response.code != 200:
            raise ValueError(response.code)

        response_dict = json.loads(response.read())
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

    def read(self, **kwargs):
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
        if self.format == 'CSV':
            return pandas.read_csv(self.url, **kwargs)
        elif self.format == 'n/a':
            raise ValueError('{0} is not available on the store'.format(self.name))
        else:
            raise ValueError('Unsupported read format: {0}'.format(self.format))