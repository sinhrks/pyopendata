# pylint: disable-msg=E1101,W0613,W0603

from __future__ import unicode_literals

import itertools
import os

import requests

import numpy as np
import pandas as pd
import pandas.compat as compat
from pandas.io.common import get_filepath_or_buffer


def _read_content(path_or_buf):
    filepath_or_buffer, _ = get_filepath_or_buffer(path_or_buf)
    if isinstance(filepath_or_buffer, compat.string_types):
        try:
            exists = os.path.exists(filepath_or_buffer)
        except (TypeError,ValueError):
            exists = False

        if exists:
            with open(filepath_or_buffer, 'r') as fh:
                data = fh.read()
        else:
            data = filepath_or_buffer
    elif hasattr(filepath_or_buffer, 'read'):
        data = filepath_or_buffer.read()
    else:
        data = filepath_or_buffer

    return data
