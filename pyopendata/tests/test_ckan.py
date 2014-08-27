# pylint: disable-msg=E1101,W0613,W0603
# coding: UTF-8

from __future__ import unicode_literals

from pyopendata import CKANStore, CKANPackage, CKANResource

import pandas.util.testing as tm


class CKANTestBase(tm.TestCase):

    _url = None
    # resource id to be used for resource test
    _resource = None
    # keyword used for search test
    _search = None

    _group = None

    # whether the site allows to search resource
    _allow_resouce = True

    def setUp(self):
        if self._url is None:
            import nose
            raise nose.SkipTest("_url is blank")
        self.store = CKANStore(self._url)

    def test_isvalid(self):
        self.assertTrue(self.store.is_valid())

    def test_search(self):
        result = self.store.search_package(self._search)
        self.assertTrue(len(result) > 0)
        self.assertTrue(isinstance(result[0], CKANPackage))

        if not self._allow_resouce:
            import nose
            raise nose.SkipTest(self._url + " doesn't allow to search resource")

        result = self.store.search_resource('name:' + self._search)
        result_names = [r.name for r in result]
        self.assertTrue(len(result) > 0)
        for resource in result:
            self.assertTrue(isinstance(resource, CKANResource))
            self.assertTrue(resource.url is not None)

        result = self.store.search('name:' + self._search)
        result_names = [r.name for r in result]
        self.assertTrue(len(result) > 0)
        for resource in result:
            self.assertTrue(isinstance(resource, CKANResource))
            self.assertTrue(resource.url is not None)

    def test_packages(self):
        packages = self.store.packages
        self.assertTrue(len(packages) > 0)
        for package in packages:
            self.assertTrue(isinstance(package, CKANPackage))
            self.assertTrue(package.name is not None)

        # Some site doesn't return resources in xml
        # In this case, CKANPackage connect to retrieve its resources
        # To avoid long waiting time, only check 1st element
        resource = packages[0].resources[0]
        self.assertTrue(isinstance(resource, CKANResource))
        self.assertTrue(resource.url is not None)

    def test_resource(self):
        if not self._allow_resouce:
            import nose
            raise nose.SkipTest(self._url + " doesn't allow to access resource")

        resource = self.store.get_resource(self._resource)
        self.assertTrue(isinstance(resource, CKANResource))
        self.assertTrue(resource.id, self._resource)
        self.assertTrue(resource.url is not None)

    def test_groups(self):
        result = self.store.groups
        self.assertTrue(self._group in result)

        packages = self.store.get_packages_from_group(self._group)
        self.assertTrue(len(packages) > 0)
        for package in packages:
            self.assertTrue(isinstance(package, CKANPackage))
            self.assertTrue(package.name is not None)

        resource = packages[0].resources[0]
        self.assertTrue(isinstance(resource, CKANResource))
        self.assertTrue(resource.url is not None)

    def test_formats(self):
        raise NotImplementedError("test_formats must be defined to check read method")


class TestCKANTestSite(CKANTestBase):

    _url = 'http://demo.ckan.org/'
    # CSV of 'average-act-scores-per-year-oklahoma-vs-united-states'
    _resource = '04127ad5-77e5-4a08-9f40-12d3c383e460'
    _search = 'gold'
    _group = 'data-explorer'

    def test_urlformat(self):
        formats = ['http://demo.ckan.org/',
                   'http://demo.ckan.org',
                   'http://demo.ckan.org/api',
                   'http://demo.ckan.org/api/']
        for url in formats:
            store = CKANStore(url)
            self.assertTrue(store.is_valid())

        # invalid URL
        store = CKANStore('http://xxxx.xxx.xxx/')
        self.assertFalse(store.is_valid())

    def test_tags(self):
        result = self.store.tags
        self.assertTrue('gold' in result)

        resources = self.store.get_resources_from_tag('gold')
        self.assertTrue(len(resources) > 0)

        resource_names = [r.name for r in resources]
        expected = ['who-data', 'gold-prices']
        self.assertTrue(resource_names, expected)

    def test_formats(self):
        package = self.store.get_package('adur_district_spending')
        for r in package.resources:
            if r.id == self._resource:
                df = r.read()
                self.assertEqual(df.shape, (564, 6))
                return
        raise ValueError('Unable to find test data for validation')

class TestDATAGOV(CKANTestBase):
    _url = 'http://catalog.data.gov/'
    _package = 'average-act-scores-per-year-oklahoma-vs-united-states'
    _resource = '434dad57-322e-430b-9b95-2cb703105cd4'
    _search = 'Oklahoma'
    _group = 'businessusa4208'

    _allow_resouce = False

    def test_groups(self):
        result = self.store.groups
        self.assertTrue('businessusa4208' in result)
        self.assertTrue('climate5434' in result)

        # Can't work now
        # packages = self.store.get_packages_from_group('climate5434')
        # self.assertTrue(len(packages) > 0)
        # for p in packages:
        #     for r in p.resources:
        #         if r.id == self._resource:
        #             df = r.read()
        #             self.assertEqual(df.shape, (564, 6))
        #             return
        # raise ValueError('Unable to find test data for validation')

    def test_tags(self):
        result = self.store.tags
        self.assertTrue('education' in result)

        resources = self.store.get_resources_from_tag('education')
        self.assertTrue(len(resources) > 0)
        for r in resources:
            if r.id == self._resource:
                df = r.resources[0].read()
                self.assertEqual(df.shape, (10, 3))
                return
        raise ValueError('Unable to find test data for validation')

    def test_formats(self):
        package = self.store.get_package(self._package)
        # JSON, CSV
        for r in package.resources:
            if r.format in CKANResource._supported_formats:
                if r.format == 'JSON':
                    # unable to create dataframe from raw json
                    pass
                else:
                    df = r.read()
                    self.assertEqual(df.shape, (10, 3))

        package = self.store.get_package('oklahoma-fy12-benefits-summary')
        # Excel
        for r in package.resources:
            print(r.format)
            if r.format in CKANResource._supported_formats:
                # ToDo: The path results in XLRD Error
                # Find better dataset
                print(r.url)
                # df = r.read()
                # self.assertEqual(df.shape, (10, 3))

    def test_raw_data(self):
        package = self.store.get_package(self._package)
        for r in package.resources:
            data = r.read(raw=True)
            self.assertTrue(len(data), 0)


class TestDATAGOJP(CKANTestBase):
    _url = 'http://www.data.go.jp/data'
    _package = 'meti_08_ds_140304_00015335'
    _resource = 'e93689c6-4c08-4fca-af31-45c61113c395'
    _search = '経済'
    _group = 'mof_07_gr_131126_00001888'

    def test_tags(self):
        result = self.store.tags
        self.assertTrue('population' in result)

        resources = self.store.get_resources_from_tag('population')
        self.assertTrue(len(resources) > 0)

    def test_formats(self):
        package = self.store.get_package(self._package)

        for r in package.resources:
            # row names differs depending on yearly / quarterly formats
            if r.format in CKANResource._supported_formats:
                df = r.read()
                if r.id in ('e93689c6-4c08-4fca-af31-45c61113c395',
                            '0f7bdfb1-161e-439f-894e-64379afbb5f4',
                            '13a96b83-1a4a-4178-80a1-a4a3f183ba45',
                            'b4fa36d2-538a-42df-89e3-ef55cb48c92f'):
                    self.assertEqual(df.shape, (302, 141))
                elif r.id in ('01a34ba2-26f1-4065-8229-be2bd4419c7c',
                              '8eb7ac30-18fa-41f9-826b-e2bbb8316f0a'):
                    self.assertEqual(df.shape, (302, 73))
                elif r.id in ('f6683af1-d8be-4967-9d9e-e7acab49ac99',
                              '0fd053be-57c1-4631-952a-9b5666b2394d'):
                    self.assertEqual(df.shape, (302, 49))
                else:
                    raise ValueError(r.id, df.shape)
            else:
                data = r.read(raw=True)
                self.assertTrue(len(data) > 0)

"""
class TestDATAGOVUK(tm.TestCase):
    _url = 'http://demo.ckan.org/'

    def setUp(self):
        self.store = CKANStore(self._url)
"""


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'], exit=False)
