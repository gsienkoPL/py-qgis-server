""" Wrapper around qgis processing context
"""

import os
import logging

from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse

from qgistools.cache.filecache import FileCache
from qgistools.utils import singleton

from .runtime import HTTPError2
from .config import get_config

LOGGER = logging.getLogger('QGSSRV')

@singleton
class _Cache(FileCache):

    def __init__(self):
        config    = get_config('cache')
        cachesize = config.getint('size')
        rootdir   = Path(config['rootdir'])

        class _Store:
            def getpath(self, key, exists=False):
                path = rootdir / key
                if not path.exists():
                    raise FileNotFoundError(str(path))

                # Get modification time for the file
                timestamp = datetime.fromtimestamp(path.stat().st_mtime)
                return str(path), timestamp

        # Init FileCache
        super().__init__(size=cachesize, store=_Store())  


def cache_lookup( path ):
    c = _Cache()
    try:
        return c.lookup(path)
    except FileNotFoundError:
        raise HTTPError2(404, "map '%s' no found" % path) 


