# pylint: disable-msg=E1101,W0613,W0603
# coding: UTF-8

from __future__ import unicode_literals

from pyopendata import (DataStore, CKANStore, OECDStore, EurostatStore,
    UNdataStore, WorldBankStore)

import pandas.util.testing as tm


class TestDataStore(tm.TestCase):

    def test_initialize(self):
        store = DataStore('oecd')
        self.assertTrue(isinstance(store, OECDStore))

        store = DataStore('eurostat')
        self.assertTrue(isinstance(store, EurostatStore))

        store = DataStore('undata')
        self.assertTrue(isinstance(store, UNdataStore))

        store = DataStore('worldbank')
        self.assertTrue(isinstance(store, WorldBankStore))

        store = DataStore('http://catalog.data.gov')
        self.assertTrue(isinstance(store, CKANStore))

        with tm.assertRaises(ValueError):
            store = DataStore('http://google.com')


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'], exit=False)
