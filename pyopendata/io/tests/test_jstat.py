# pylint: disable-msg=E1101,W0613,W0603

import os

import numpy as np
import pandas as pd
from pandas.compat import range
import pandas.util.testing as tm

from pyopendata.io import read_jstat


class TestJStat(tm.TestCase):

    def setUp(self):
      self.dirpath = tm.get_data_path()

    def test_hierarchy(self):
        result = read_jstat(os.path.join(self.dirpath, 'jstat', 'hierarchy.json'))
        self.assertTrue(isinstance(result, pd.DataFrame))
        result = result.head(n=10)

        idx = pd.Index(['Total', 'Food and non-alcoholic beverages', 'Bread and cereal products',
               'Bread', 'Cakes and biscuits', 'Breakfast cereals', 'Other cereal products',
               'Meat and seafoods', 'Beef and veal', 'Pork'], name='commodity')
        expected = pd.DataFrame([np.nan] * 10, index=idx)

        tm.assert_frame_equal(result, expected)

    def test_oecd_canada(self):
        results = read_jstat(os.path.join(self.dirpath, 'jstat', 'oecd-canada.json'))
        self.assertEqual(len(results), 2)

        result = results['oecd'].head(n=5)
        exp_idx = pd.MultiIndex.from_product([['Unemployment rate'],
                                              ['Australia', 'Austria', 'Belgium', 'Canada', 'Chile']],
                                             names=['concept', 'area'])
        exp_col = pd.Index(['2003', '2004', '2005', '2006', '2007', '2008', '2009',
                            '2010', '2011', '2012', '2013', '2014'], name='year')

        values = np.array([[5.94382629, 5.39663128, 5.04479059, 4.78936279,
                            4.37964939, 4.24909345, 5.5922266, 5.23066029,
                            5.09942294, 5.22433609, 5.50415003, 5.46286623],
                           [4.27855934, 4.93970775, 5.15216061, 4.72718286,
                            4.39973073, 3.81393363, 4.77691251, 4.39159165,
                            4.14358724, 4.35134579, 4.69549171, 4.74532331],
                           [8.15833333, 8.4, 8.48333333, 8.26666667,
                            7.46666667, 7.01666667, 7.89189286, 8.28317196,
                            7.17513878, 7.3811534, 7.6895529, 7.73544264],
                           [7.59461675, 7.16783395, 6.7486915, 6.3078411,
                            6.04984263, 6.14601466, 8.2846893, 7.98890042,
                            7.4536096, 7.32358421, 7.16974153, 6.88122705],
                           [9.5433848, 10.00149582, 9.22442255, 7.77316628,
                            7.15062335, 7.7872218, 10.80236438, 8.12157908,
                            7.10477825, 6.47746872, 6.78101031, 6.78019894]])
        expected = pd.DataFrame(values, index=exp_idx, columns=exp_col)
        tm.assert_frame_equal(result, expected)

        result = results['canada'].head(n=6)
        exp_idx = pd.MultiIndex.from_product([['Canada'], ['2012'],
                                              ['0 to 4', '10 to 14', '15 to 19'],
                                              ['% of total of each group', 'Persons (thousands)']],
                                             names=['country', 'year', 'age', 'concept'])
        exp_col = pd.Index(['Female', 'Male', 'Total'], name='sex')

        values = np.array([[5.3, 5.7, 5.5],
                           [940.1, 988.7, 1928.8],
                           [5.2, 5.6, 5.4],
                           [912.6, 964.7, 1877.3],
                           [6, 6.4, 6.2],
                           [1054.7, 1108.2, 2163]])
        expected = pd.DataFrame(values, index=exp_idx, columns=exp_col)
        tm.assert_frame_equal(result, expected)

    def test_order(self):
        result = read_jstat(os.path.join(self.dirpath, 'jstat', 'order.json'))
        exp_idx = pd.MultiIndex.from_product([['1', '2', '3'], ['1', '2']], names=['A', 'B'])
        exp_col = pd.Index(['1', '2', '3', '4'], name='C')
        expected = pd.DataFrame({'1': ['A1B1C1', 'A1B2C1', 'A2B1C1', 'A2B2C1', 'A3B1C1', 'A3B2C1'],
                                 '2': ['A1B1C2', 'A1B2C2', 'A2B1C2', 'A2B2C2', 'A3B1C2', 'A3B2C2'],
                                 '3': ['A1B1C3', 'A1B2C3', 'A2B1C3', 'A2B2C3', 'A3B1C3', 'A3B2C3'],
                                 '4': ['A1B1C4', 'A1B2C4', 'A2B1C4', 'A2B2C4', 'A3B1C4', 'A3B2C4']},
                                index=exp_idx, columns=exp_col)
        tm.assert_frame_equal(result, expected)

        result = read_jstat(os.path.join(self.dirpath, 'jstat', 'order.json'), typ='series')
        exp_idx = pd.MultiIndex.from_product([['1', '2', '3'], ['1', '2'],
                                              ['1', '2', '3', '4']], names=['A', 'B', 'C'])
        expected = pd.Series(['A1B1C1', 'A1B1C2', 'A1B1C3', 'A1B1C4',
                              'A1B2C1', 'A1B2C2', 'A1B2C3', 'A1B2C4',
                              'A2B1C1', 'A2B1C2', 'A2B1C3', 'A2B1C4',
                              'A2B2C1', 'A2B2C2', 'A2B2C3', 'A2B2C4',
                              'A3B1C1', 'A3B1C2', 'A3B1C3', 'A3B1C4',
                              'A3B2C1', 'A3B2C2', 'A3B2C3', 'A3B2C4'], index=exp_idx)
        tm.assert_series_equal(result, expected)

        result = read_jstat(os.path.join(self.dirpath, 'jstat', 'order.json'), squeeze=False)
        self.assertTrue(isinstance(result, dict))
        result = result['order']
        exp_idx = pd.MultiIndex.from_product([['1', '2', '3'], ['1', '2']], names=['A', 'B'])
        exp_col = pd.Index(['1', '2', '3', '4'], name='C')
        expected = pd.DataFrame({'1': ['A1B1C1', 'A1B2C1', 'A2B1C1', 'A2B2C1', 'A3B1C1', 'A3B2C1'],
                                 '2': ['A1B1C2', 'A1B2C2', 'A2B1C2', 'A2B2C2', 'A3B1C2', 'A3B2C2'],
                                 '3': ['A1B1C3', 'A1B2C3', 'A2B1C3', 'A2B2C3', 'A3B1C3', 'A3B2C3'],
                                 '4': ['A1B1C4', 'A1B2C4', 'A2B1C4', 'A2B2C4', 'A3B1C4', 'A3B2C4']},
                                index=exp_idx, columns=exp_col)
        tm.assert_frame_equal(result, expected)

    def test_omit_values(self):
        result = read_jstat(os.path.join(self.dirpath, 'jstat', 'omit-values.json'))
        exp_idx = pd.MultiIndex.from_product([['1', '2', '3'], ['1', '2']], names=['A', 'B'])
        exp_col = pd.Index(['1', '2', '3', '4'], name='C')
        expected = pd.DataFrame({'1': ['A1B1C1', 'A1B2C1', 'A2B1C1', 'A2B2C1', 'A3B1C1', 'A3B2C1'],
                                 '2': [np.nan, np.nan, np.nan, np.nan, np.nan, 'A3B2C2'],
                                 '3': [np.nan, 'A1B2C3', np.nan, np.nan, np.nan, np.nan],
                                 '4': [np.nan, np.nan, np.nan, 'A2B2C4', np.nan, np.nan]},
                                index=exp_idx, columns=exp_col)
        tm.assert_frame_equal(result, expected)

    def test_us_gsp(self):
        result = read_jstat(os.path.join(self.dirpath, 'jstat', 'us-gsp.json'))
        result = result.head(n=10)

        exp_idx = pd.MultiIndex.from_product([['2013'],
                                              ['Alabama', 'Alaska', 'Arizona', 'Arkansas',
                                               'California', 'Colorado', 'Connecticut',
                                               'Delaware', 'District of Columbia', 'Florida']],
                                             names=['year', 'state'])
        exp_col = pd.Index(['Gross State Product', 'Gross State Product as percentage of national GDP',
                            'Gross State Product per capita', 'Population'], name='concept')

        values = np.array([[174400, 1.2, 36333, 4.8],
                           [45600, 0.31, 65143, 0.7],
                           [261300, 1.8, 40828, 6.4],
                           [105800, 0.73, 36483, 2.9],
                           [2080600, 13.34, 51914, 37.3],
                           [259700, 1.79, 51940, 5],
                           [233400, 1.61, 64833, 3.6],
                           [62700, 0.43, 69667, 0.9],
                           [104700, 0.72, 174500, 0.6],
                           [754000, 5.2, 40106, 18.8]])
        expected = pd.DataFrame(values, index=exp_idx, columns=exp_col)
        tm.assert_frame_equal(result, expected)

    def test_us_labor(self):
        result = read_jstat(os.path.join(self.dirpath, 'jstat', 'us-labor.json'))
        result = result.head(n=10)

        exp_idx = pd.MultiIndex.from_product([['2012'],
                                              ['Abbeville County, SC', 'Acadia Parish, LA',
                                               'Accomack County, VA', 'Ada County, ID',
                                               'Adair County, IA', 'Adair County, KY',
                                               'Adair County, MO', 'Adair County, OK',
                                               'Adams County, CO', 'Adams County, IA']],
                                             names=['year', 'county'])
        exp_col = pd.Index(['Employed', 'Labor Force', 'Unemployed',
                            'Unemployment rate'], name='labor')

        values = np.array([[9757, 10861, 1104, 10.2],
                           [24391, 25826, 1435, 5.6],
                           [16958, 18215, 1257, 6.9],
                           [191379, 204182, 12803, 6.3],
                           [4134, 4317, 183, 4.2],
                           [8886, 9631, 745, 7.7],
                           [11480, 12219, 739, 6.0],
                           [9747, 10476, 729, 7.0],
                           [212762, 234436, 21674, 9.2],
                           [1999, 2090, 91, 4.4]])
        expected = pd.DataFrame(values, index=exp_idx, columns=exp_col)
        tm.assert_frame_equal(result, expected)

    def test_us_unr(self):
        result = read_jstat(os.path.join(self.dirpath, 'jstat', 'us-unr.json'))
        result = result.head(n=10)

        exp_idx = pd.MultiIndex.from_product([['2012'],
                                              ['01001', '01003', '01005', '01007', '01009',
                                               '01011', '01013', '01015', '01017', '01019']],
                                             names=['year', 'county'])
        exp_col = pd.Index(['Unemployment rate'], name='labor')
        expected = pd.DataFrame({'Unemployment rate': [6.5, 6.8, 11.2, 7.6, 6.2,
                                                       13.4, 10.9, 7.6, 9.3, 7.1]},
                                index=exp_idx, columns=exp_col)
        tm.assert_frame_equal(result, expected)


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'], exit=False)
