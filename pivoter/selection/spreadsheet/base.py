import copy
import logging
from typing import List

from pivoter.models.source.cell import BaseCell
from pivoter.utils import cellutils

from .. import datafuncs as dfc
from ..base import Selectable


class BaseSpreadsheetSelectable(Selectable):
    """
    Class representing a spreadsheet input, holding
    all methods commmon to spreadsheets of whatever
    flavour.
    """

    ...
