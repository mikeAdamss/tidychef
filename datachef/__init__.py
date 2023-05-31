"""
Code relating to the reading in of data sources.
.. include:: ../_docs/splashpage.md
"""

from datachef.cardinal.directions import down, left, right, up, above, below
from datachef.readers.acquire import acquire
from datachef.selection import filters
from datachef.utils.preview.previewer import label, preview

from . import models, utils
