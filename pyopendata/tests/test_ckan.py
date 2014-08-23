# pylint: disable-msg=E1101,W0613,W0603

from pyopendata import CKANStore, CKANPackage, CKANResource

import pandas.util.testing as tm

"""
class TestCKANTestSite(tm.TestCase):
    _url = 'http://demo.ckan.org/'
    _resource = '04127ad5-77e5-4a08-9f40-12d3c383e460'

    def setUp(self):
        self.store = CKANStore(self._url)

    def test_isvalid(self):
        self.assertTrue(self.store.is_valid())

    def test_urlformat(self):
        formats = ['http://demo.ckan.org/',
                   'http://demo.ckan.org',
                   'http://demo.ckan.org/api',
                   'http://demo.ckan.org/api/']
        for url in formats:
            store = CKANStore(url)
            self.assertTrue(store.is_valid())

    def setUp(self):
        self.store = CKANStore(self._url)

    def test_isvalid(self):
        self.assertFalse(self.store.is_valid())

    def test_packages(self):
        result = self.store.packages
        self.assertTrue('adur_district_spending' in result)

        package = self.store.get_package('adur_district_spending')
        for r in package.resources:
            if r.id == self._resource:
                df = r.read()
                self.assertEqual(df.shape, (564, 6))
                return
        raise ValueError('Unable to find test data for validation')

    def test_resource(self):
        # CSV of 'average-act-scores-per-year-oklahoma-vs-united-states'
        resource = self.store.get_resource(self._resource)
        self.assertTrue(resource.id, self._resource)

    def test_groups(self):
        result = self.store.groups
        self.assertTrue('data-explorer' in result)

        packages = self.store.get_packages_from_group('data-explorer')
        self.assertTrue(len(packages) > 0)
        for p in packages:
            for r in p.resources:
                if r.id == '04127ad5-77e5-4a08-9f40-12d3c383e460':
                    df = r.read()
                    self.assertEqual(df.shape, (564, 6))
                    return
        raise ValueError('Unable to find test data for validation')

    def test_tags(self):
        result = self.store.tags
        self.assertTrue('gold' in result)

        resources = self.store.get_resources_from_tag('gold')
        self.assertTrue(len(resources) > 0)

        resource_names = [r.name for r in resources]
        expected = ['who-data', 'gold-prices']
        self.assertTrue(resource_names, expected)


class TestInvalidTestSite(tm.TestCase):
    _url = 'http://xxxx.xxx.xxx/'

    def setUp(self):
        self.store = CKANStore(self._url)

    def test_isvalid(self):
        self.assertFalse(self.store.is_valid())
"""

class TestDATAGOV(tm.TestCase):
    _url = 'http://catalog.data.gov/'
    _resource = '434dad57-322e-430b-9b95-2cb703105cd4'

    def setUp(self):
        self.store = CKANStore(self._url)

    def test_isvalid(self):
        self.assertTrue(self.store.is_valid())

    def test_packages(self):
        result = self.store.packages
        result_names = [r.name for r in result]
        self.assertTrue('consumer-complaint-database' in result_names)

        package = self.store.get_package('average-act-scores-per-year-oklahoma-vs-united-states')
        df = package.resources[0].read()
        self.assertEqual(df.shape, (10, 3))

    def test_resource(self):
        # Can't work for data.gov

        # CSV of 'average-act-scores-per-year-oklahoma-vs-united-states'
        # resource = self.store.get_resource('61e12273-4d1b-4176-8469-ac4eb6394502')
        # df = resources.read()
        # self.assertEqual(df.shape, (10, 3))
        pass

    def test_groups(self):
        result = self.store.groups
        self.assertTrue('businessusa4208' in result)
        self.assertTrue('climate5434' in result)

        # Can't work now
        # packages = self.store.get_packages_from_group('climate5434')
        # self.assertTrue(len(packages) > 0)
        # for p in packages:
        #     for r in p.resources:
        #         if r.id == '04127ad5-77e5-4a08-9f40-12d3c383e460':
        #             df = r.read()
        #             self.assertEqual(df.shape, (564, 6))
        #             return
        # raise ValueError('Unable to find test data "04127ad5-77e5-4a08-9f40-12d3c383e460"')

    def test_tags(self):
        result = self.store.tags
        self.assertTrue('education' in result)

        resources = self.store.get_resources_from_tag('education')
        self.assertTrue(len(resources) > 0)
        for r in resources:
            # average-act-scores-per-year-oklahoma-vs-united-states
            if r.id == self._resource:
                df = r.resources[0].read()
                self.assertEqual(df.shape, (10, 3))
                return
        raise ValueError('Unable to find test data for validation')

    def test_formats(self):
        package = self.store.get_package('average-act-scores-per-year-oklahoma-vs-united-states')
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
        package = self.store.get_package('average-act-scores-per-year-oklahoma-vs-united-states')
        for r in package.resources:
            data = r.read(raw=True)
            self.assertTrue(len(data), 0)


"""
class TestDATAGOVUK(tm.TestCase):
    _url = 'http://demo.ckan.org/'

    def setUp(self):
        self.store = CKANStore(self._url)
"""
# cstore = pyod.base.CKANStore('http://catalog.data.gov/')


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'], exit=False)
