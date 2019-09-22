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

# Variables to be used primarily by the Task reader.
# (Gather depending on the type of input expected.)
FILE = 'file'           # string - path
SAVE = 'save'           # string - path
DATETIME = 'datetime'   # string to inform engine for the header of date-time data
TIMEFROM = 'timefrom'   # string to limit data porcessing based on time
TIMETO = 'timeto'       # string to limit data porcessing based on time

NODATA = 'nodata'       # string or comma-separated strings (might not be used, will use try-except functionality...)
VEC = 'vec'             # string or comma-separated strings
SCAL = 'scal'           # string
FTYPE = 'ftype'         # string or comma-separated strings

HISTO = 'histo'         # logical
SCATT = 'scatter'       # logical
ROSE = 'rose'           # logical
HEAT = 'heat'           # logical
STATS = 'stats'         # logical
SERIES = 'series'       # logical
METEO = 'meteo'         # logical

DPI = 'dpi'             # numeric (int)
FIGSIZE = 'figsize'     # numeric (float), one or two values
TFONT = 'titlefont'     # numeric (int)
LFONT = 'labelfont'     # numeric (int)

NOKEY = 'nokey'         # Not expected in the conf file, just as a no-key flag for the rest of the code
NOKEY_val = ''

# List the keys above
KEYS_str = {
    FILE: '',
    SAVE: '',
    DATETIME: 'datetime',
    TIMEFROM: '',
    TIMETO: ''
}

KEYS_mult_str = {
    NODATA: ['null'],
    VEC: [],
    SCAL: [],
    FTYPE: ['png']
}

KEYS_bool = {
    HISTO: False,
    SCATT: False,
    ROSE: False,
    HEAT: False,
    STATS: False,
    SERIES: False,
    METEO: True             # Gotcha! On by default, meteorological convention for directions
}

KEYS_num = {
    DPI: 150,
    TFONT: 17,
    LFONT: 14
}

KEYS_mult_num = {
    FIGSIZE: (10, 10)
}

POS_ANS = ['1', 't', 'y', 'yes', 'true']
FTYPES_ALLOWED = ['png', 'eps', 'pdf', 'ps', 'svg']

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