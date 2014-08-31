# pylint: disable-msg=E1101,W0613,W0603

from __future__ import unicode_literals

import os

import requests

import numpy as np
import pandas as pd
import pandas.compat as compat

from pyopendata.io.util import _read_content


def read_jstat(path_or_buf, typ='frame', squeeze=True):
    """
    Convert a JSON-Stat string to pandas object

    Parameters
    ----------
    filepath_or_buffer : a valid JSON-Stat string or file-like
        http://json-stat.org/

    typ : {'frame', 'series'}
        Type of object to recover (series or frame), default 'frame'

    squeeze : bool, default True
        If True, return DataFrame or Series when the input has only one dataset.
        When the input has multiple dataset, returns dictionary of results.
        If False, always return a dictionary.

    Returns
    -------
    results : Series, DataFrame, or dictionaly of Series or DataFrame.
    """

    jdata = _read_content(path_or_buf)

    import json
    if isinstance(jdata, dict):
        datasets = jdata
    else:
        datasets = json.loads(jdata, object_pairs_hook=compat.OrderedDict)

    results = {}
    for dataname, dataset in compat.iteritems(datasets):
        values = dataset['value']               # mandatory
        dimensions = dataset['dimension']       # mandatory
        # Not supported, as the reis no specific meaning
        # in current format specification
        # status = dataset.get('status', None)    # optional
        midx = _parse_dimensions(dimensions)
        values = _parse_values(values, size=len(midx))

        result = pd.Series(values, index=midx)
        if typ == 'frame':
            if result.index.nlevels > 1:
                result = result.unstack()
            else:
                result = result.to_frame()
        elif typ == 'series':
            pass
        else:
            raise ValueError("'typ' must be either 'frame' or 'series'")
        if len(datasets) == 1 and squeeze:
            return result

        results[dataname] = result
    return results


def _parse_values(values, size):
    if isinstance(values, list):
        return values
    elif isinstance(values, dict):
        result = [np.nan] * size
        for k, v in compat.iteritems(values):
            result[int(k)] = v
        return result
    else:
        raise ValueError("'values' must be list or dict")


def _parse_dimensions(dimensions):
    names = dimensions['id']
    sizes = dimensions['size']
    arrays = []
    for name in names:
        dimension = dimensions[name]            # mandatory
        # roles = dimensions.get('role', None)  # optional
        categories = dimension['category']      # mandatory
        index = None

        if 'index' not in categories and 'label' not in categories:
            # index is required unless the dimension is a constant dimension
            # In the case that a category index is not provided,
            # a category label must be included.
            raise ValueError("Input must have 'index' or 'label' attribute")

        if 'index' in categories:
            index = categories['index']
            if isinstance(index, list):
                pass
            elif isinstance(index, dict):
                sorted_index = []
                for k, v in sorted(index.items(), key=lambda x:x[1]):
                    sorted_index.append(k)
                index = sorted_index
            else:
                raise ValueError("'index' must be list or dict, "
                                 "{0} given".format(type(index)))

        if 'label' in categories:
            labels = categories['label']
            if isinstance(labels, dict):
                if index is None:
                    if len(labels) == 1:
                        index = list(labels.values())
                    else:
                        raise ValueError("'index' is required to match multiple labels")
                else:
                    index = [labels[i] for i in index]
            else:
                raise ValueError("'label' must be dict, "
                                 "{0} given".format(type(labels)))

        arrays.append(index)

    midx = pd.MultiIndex.from_product(arrays, names=names)
    return midx
