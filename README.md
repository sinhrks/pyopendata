# pyopendata

![Travis-CI Build Status](https://travis-ci.org/sinhrks/pyopendata.svg)

## Overview

``pyopendata`` is an Python utility to offer an unified API to wolrd various data sources,
outputs ``pandas.DataFrame`` format.

## Installation

```sh
pip install pyopendata
```

## Usage

    >>> import pyopendata as pyod

    # You can create datastore for access by passing URL.
    >>> store = pyod.CKANStore('http://catalog.data.gov/')
    >>> store
    CKANStore (http://catalog.data.gov)

    # Perform search by keywords. Results will be the list of datasets.
    >>> results = store.search('department of health')
    >>> results
    [job-openings-and-labor-turnover-survey-f70f4 (1 resource),
     business-identification-numbers-cross-referencing-bincs-system (1 resource),
     american-community-survey (1 resource), ...]

    # You can access to the dataset by slicing.
    >>> results[0]
    job-openings-and-labor-turnover-survey-f70f4 (1 resource)

    # Or get datastore specifying name.
    >>> package = store.get('survey-summary')
    >>> package
    survey-summary (4 resources)

    # Dataset contains resources which contains actual data
    >>> package.resources[0]
    Resource ID: 56969e54-244f-4022-b2f4-6f648bc749f5
    Resource Name: Comma Separated Values File
    Resource URL: https://data.medicare.gov/api/views/tbry-pc2d/rows.csv?accessType=DOWNLOAD
    Format: CSV, Size: None

    # Call read method to get data as pandas DataFrame format.
    >>> package.resources[0].read()
                                                    Location  Processing Date
    0      701 MONROE STREET NW\nRUSSELLVILLE, AL 35653\n...       08/01/2014
    1      701 MONROE STREET NW\nRUSSELLVILLE, AL 35653\n...       08/01/2014
    2      701 MONROE STREET NW\nRUSSELLVILLE, AL 35653\n...       08/01/2014

    [46484 rows x 47 columns]

    # Or can get raw data by passing raw keyword
    >>> package.resources[0].read(raw=True)
    Federal Provider Number,Provider Name, ....
    015009,"BURNS NURSING HOME, INC." ...

