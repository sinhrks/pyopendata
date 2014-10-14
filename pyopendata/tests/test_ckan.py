# pylint: disable-msg=E1101,W0613,W0603
# coding: UTF-8

from __future__ import unicode_literals

from pyopendata import CKANStore, CKANPackage, CKANResource

import numpy as np
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

        package = packages[0]

        # Some site doesn't return resources in xml
        # In this case, CKANPackage connect to retrieve its resources
        # To avoid long waiting time, only check 1st element
        resource = package.resources[0]
        self.assertTrue(isinstance(resource, CKANResource))
        self.assertTrue(resource.url is not None)

        got_resource = package.get(resource.id)
        self.assertEqual(got_resource.id, resource.id)

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
        store = CKANStore('http://google.com/')
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
    # _package = 'meti_08_ds_140304_00015335'
    _package = 'soumu_20140909_0696'
    # _resource = 'e93689c6-4c08-4fca-af31-45c61113c395'
    _resource = '8933bba5-2cbd-4354-b763-0d1439cac8e3'
    _search = '経済'
    _group = 'gr_0100'

    def test_isvalid(self):
        # site_read is disabled in data.go.jp
        self.assertTrue(not self.store.is_valid())

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
                if r.id == 'c67b60d6-1fed-478b-9219-1dd98a3691ec':
                    # csv has incorrect format
                    continue
                df = r.read()
                self.assertEqual(df.shape, (15, 18))
            else:
                data = r.read(raw=True)
                self.assertTrue(len(data) > 0)

    def test_mining_manufacture(self):
        # 鉱工業指数の取得テスト
        # http://sinhrks.hatenablog.com/entry/2014/10/06/222110
        resource = self.store.get('aad25837-7e83-4881-9372-1839ecb9b5eb')

        expected = {
            '在庫': np.array(['2A00000000', '製造工業', 9988.1,
                121.2, 120.9, 109.2, 109.3, 113.3, 114.2, 116.2,
                116, 113.4, 119.3, 123.1, 121.9, 125.8, 119.7, 104.9, 104, 105.5, 103.2,
                103.7, 103.1, 99.3, 100.8, 102.9, 100.5, 104.7, 105.3, 93.9, 96.2, 99.8,
                98.6, 99.4, 98.8, 96.7, 101.1, 102.7, 102.9, 109, 107.6, 92.1, 95.4, 103.8,
                103.4, 105.8, 107.7, 104.5, 108.1, 109.3, 105, 110.8, 110.5, 103.3, 107,
                109.3, 108.9, 112.5, 113.4, 110, 113.7, 114.7, 110.5, 114.3, 111, 100.2,
                102.4, 106.3,105.7, 109.4, 109.5, 106.2, 109.6, 108.8, 105.7, 109.8, 107.2,
                98.7, 100.5, 107.2, 108.7, 112.6, 114.6], dtype=object),
            '出荷': np.array(['2A00000000', '製造工業', 9985.7,
                108.9, 117.0, 130.4, 109.6, 107.5, 115.1, 116.8, 101.2, 117.6,
                108.9, 99.1, 95.1, 75.3, 74.7, 88.4, 75.9, 75.2, 88.9, 90.8, 82.0, 97.9, 95.4,
                95.6, 99.0, 89.0, 95.0, 113.6, 95.3, 90.5, 103.8, 103.8, 94.4, 110.2, 98.0,
                102.6, 103.8, 91.4, 98.0, 98.8, 78.7, 82.3, 101.4, 100.0, 95.1, 107.1, 99.5,
                99.8, 102.7, 91.4, 101.0, 113.4, 94.0, 93.7, 101.7, 100.3, 92.5, 98.5, 94.4, 93.8,
                94.7, 87.3, 92.3, 106.9, 91.2, 91.6, 96.4, 101.8, 91.2, 103, 100.3, 100, 100.8, 95.5,
                98.3, 113.9, 93.4, 90.9, 98.5, 101.6, 88], dtype=object),
            '生産': np.array(['2A00000000', '製造工業',
                9978.9, 108.5, 117.0, 125.3, 111.0, 108.7, 115.9, 117.9, 101.2, 116.9, 111.7, 100.6,
                93.6, 76.5, 73.5, 84.2, 77.6, 77.3, 89.3, 91.3, 82.3, 96.0, 95.7, 96.6, 97.6, 88.8,
                94.7, 108.9, 96.2, 92.1, 103.9, 104.8, 95.7, 108.4, 100.3, 103.2, 102.9, 92.6, 98.5,
                94.4, 83.3, 87.4, 102.4, 102.1, 96.7, 105.2, 101.8, 100.7, 101.0, 92.8, 101.5, 110.1,
                95.9, 94.0, 101.9, 102.2, 92.7, 97.1, 97.0, 95.2, 93.2, 86.9, 91.3, 102.4, 92.8, 93.1,
                97, 104.1, 92.1, 102.2, 102.3, 99.8, 100, 96.1, 97.8, 110, 96.3, 94, 100, 103.4, 89.4],
                dtype=object)}

        for i, sheet in enumerate(expected):
            # check cache
            if i == 0:
                self.assertTrue(resource._raw_content is None)

            # Failed in Python 3
            # else:
            #     self.assertTrue(resource._raw_content is not None)

            df = resource.read(sheetname=sheet, skiprows=[0, 1])
            self.assertEqual(df.shape, (150, 83))
            tm.assert_almost_equal(df.loc[1].values, expected[sheet])


"""
class TestDATAGOVUK(tm.TestCase):
    _url = 'http://demo.ckan.org/'

    def setUp(self):
        self.store = CKANStore(self._url)
"""


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'], exit=False)
