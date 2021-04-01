"""
GQL-API wrapper
~~~~~~~~~~~~~~~~~~~

A gql wrapper for the dclist.net API.

:copyright: (c) 2021-present ilkergzlkkr
:license: MIT, see LICENSE for more details.

"""

__title__ = 'dclist.py'
__author__ = 'ilkergzlkkr'
__copyright__ = 'Copyright 2021-present ilkergzlkkr'
__license__ = 'MIT'
__version__ = '0.1.2'

from collections import namedtuple
VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')
version_info = VersionInfo(major=0, minor=1, micro=2, releaselevel='final', serial=0)

version_info = f'{version_info.major}.{version_info.minor}.{version_info.micro}'

from .client import DCLClient
from .gqlhttp import GQLHTTPClient
from .errors import *