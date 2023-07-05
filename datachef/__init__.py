"""
Code relating to the reading in of data sources.
.. include:: ../_docs/splashpage.md
"""
from datachef.cardinal.directions import above, below, down, left, right, up
from datachef.column.column import Column
from datachef.notebook.preview.html.main import preview
from datachef.output.tidydata import TidyData
from datachef.selection import filters
from datachef.selection.csv.csv import CsvSelectable
from datachef.selection.selectable import Selectable
from datachef.selection.xls.xls import XlsSelectable
from datachef.selection.xlsx.xlsx import XlsxSelectable
from datachef.validation.matcher import matches

from . import acquire, models, notebook, utils
