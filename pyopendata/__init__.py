# pylint: disable-msg=E1101,W0613,W0603
import pyopendata.io
from pyopendata.base import DataStore, DataResource
from pyopendata.ckan import CKANStore, CKANPackage, CKANResource
from pyopendata.eurostat import EurostatStore, EurostatResource
from pyopendata.oecd import OECDStore, OECDResource
from pyopendata.undata import UNdataStore, UNdataResource
from pyopendata.worldbank import WorldBankStore, WorldBankResource

from pyopendata.version import version as __version__