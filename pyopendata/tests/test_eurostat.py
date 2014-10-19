# pylint: disable-msg=E1101,W0613,W0603

from pyopendata import EurostatStore, EurostatResource

import numpy as np
import pandas as pd
from pandas.compat import range
import pandas.util.testing as tm


class TestEurostatTestSite(tm.TestCase):

    def setUp(self):
        self.store = EurostatStore()

    def test_isvalid(self):
        self.assertTrue(self.store.is_valid())

    def test_datasets(self):
        resources = self.store.datasets

        tested = False
        for resource in resources:
            self.assertTrue(isinstance(resource, EurostatResource))

            if resource.id == 'cdh_e_fos':
                df = resource.read()
                self.assertTrue(isinstance(df, pd.DataFrame))
                self.assertEqual(df.shape, (2, 336))
                tested = True

        self.assertTrue(tested)

    def test_get_cdh_e_fos(self):
        # Employed doctorate holders in non managerial and non professional
        # occupations by fields of science (%)
        resource = self.store.get('cdh_e_fos')
        self.assertTrue(isinstance(resource, EurostatResource))
        df = resource.read()

        self.assertTrue(isinstance(df, pd.DataFrame))
        self.assertEqual(df.shape, (2, 336))

        df = df['Percentage']['Total']['Natural sciences']
        df = df[['Norway', 'Poland', 'Portugal', 'Russia']]

        exp_col = pd.MultiIndex.from_product([['Norway', 'Poland', 'Portugal', 'Russia'],
                                              ['Annual']],
                                             names=['GEO', 'FREQ'])
        exp_idx = pd.DatetimeIndex(['2006', '2009'], name='TIME_PERIOD')

        values = np.array([[25.49, np.nan, 39.05, np.nan],
                           [20.38, 25.1, 27.77, 38.1]])
        expected = pd.DataFrame(values, index=exp_idx, columns=exp_col)
        tm.assert_frame_equal(df, expected)

        raw_data = resource.read(raw=True)
        self.assertTrue(len(raw_data) > 0)

    def test_get_sts_cobp_a(self):
        # Building permits - annual data (2010 = 100)
        resource = self.store.get('sts_cobp_a')
        self.assertTrue(isinstance(resource, EurostatResource))
        df = resource.read()

        self.assertTrue(isinstance(df, pd.DataFrame))
        self.assertEqual(df.shape, (22, 684))

        idx = pd.DatetimeIndex(['1992', '1993', '1994', '1995', '1996', '1997',
                                '1998', '1999', '2000', '2001', '2002', '2003',
                                '2004', '2005', '2006', '2007', '2008', '2009',
                                '2010', '2011', '2012', '2013'], name='TIME_PERIOD')
        ne = pd.Series([np.nan, np.nan, np.nan, 144.55, 137.02, 180.22, 198.51,
                        215.07, 199.97, 186.34, 127.39, 130.78, 143.35, 147.96,
                        176.78, 227.75, 199.62, 128.52, 100.09, 113.92, 89.31,
                        77.62],
                       name=('Building permits - m2 of useful floor area',
                             'Gross data',
                             'Non-residential buildings, except office buildings',
                             'Netherlands', 'Annual'),
                       index=idx)

        uk = pd.Series([np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 120.4,
                        115.94, 112.54, 113.34, 110.2, 112.17, 119.07, 112.71,
                        113.06, 121.87, 113.99, 105.89, 99.99, 98.54, 103.72,
                        81.32],
                       name=('Building permits - m2 of useful floor area',
                             'Gross data',
                             'Non-residential buildings, except office buildings',
                             'United Kingdom', 'Annual'),
                       index=idx)
        for expected in [ne, uk]:
            result = df[expected.name]['1992':'2013']
            print(result.values)
            # tm.assert_series_equal(result, expected)


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'], exit=False)
