"""
Just a module to share data structures
or variables commonly used.
"""

# Variables to be used primarily
# by the SKIRON data reader.
DIR = 'dir'
MAG = 'mag'

MEAN = 'mean'
MIN = 'min'
MAX = 'max'
MEDIAN = 'median'
STD = 'std'
PRCTILES = 'prctiles'
COV = 'covariance'
RECORDS = 'records'

ptiles = [10, 20, 40, 60, 80, 90]
STAT_ID = [MEAN, MIN, MAX, MEDIAN, STD, COV, PRCTILES, RECORDS]

# Variables to be used primarily
# by the Task reader.
FILE = 'file'
NODATA = 'nodata'
VEC = 'vec'
SCAL = 'scal'
HISTO = 'histo'
SCATT = 'scatter'
ROSE = 'rose'
HEAT = 'heat'
STATS = 'stats'
SERIES = 'series'
SAVE = 'save'
FTYPE = 'ftype'
METEO = 'meteo'
NOKEY = 'nokey'

KEYS = [
    FILE,
    NODATA,
    VEC,
    SCAL,
    HISTO,
    SCATT,
    ROSE,
    HEAT,
    STATS,
    SERIES,
    SAVE,
    FTYPE,
    METEO,
    NOKEY
]

INIT_DICT = {
    FILE: '',
    NODATA: [],
    VEC: [],
    SCAL: [],
    HISTO: False,
    SCATT: False,
    ROSE: False,
    HEAT: False,
    STATS: False,
    SERIES: False,
    SAVE: '',
    FTYPE: [],
    METEO: True
}

DEF_VALS = {
    FILE: '',
    NODATA: ['null'],
    VEC: [],
    SCAL: [],
    HISTO: False,
    SCATT: False,
    ROSE: False,
    HEAT: False,
    STATS: False,
    SERIES: False,
    SAVE: 'results',
    FTYPE: ['png'],
    METEO: True,
    NOKEY: ''
}

POS_ANS = ['1', 't', 'y', 'yes', 'true']
FTYPES_ALLOWED = ['png', 'jpg', 'jpeg']

# This section defines the dictionaries
# to help when annotating the figures.
description_dict = {
    MAG: 'Wind speed',
    DIR: 'Wind direction',
    'u': 'Wind (x-comp)',
    'v': 'Wind (y-comp)',
    'aird': 'Air density',
    'p': 'Pressure',
    't': 'Temperature',
    'q2': 'Humidity',
    'smll': 'unknown'
}

units_dict = {
    MAG: 'm/s',
    DIR: 'deg from North',
    'u': 'm/s',
    'v': 'm/s',
    'aird': 'kg/m^3',
    'p': 'Pa',
    't': 'K',
    'q2': 'e',
    'smll': 'units'
}

level_dict = {
    'm1ll': '10 m',
    'm2ll': '40 m',
    'm3ll': '80 m',
    'm4ll': '120 m',
    'm5ll': '160 m'
}

graph_types = {
    SCATT: 'Components',
    HISTO: 'Histogram',
    ROSE: 'Rose Chart',
    HEAT: 'Heatmap',
    SERIES: 'Timeseries'
}