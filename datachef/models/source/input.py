"""
Classes representing a single input.

An input would be a single tabulated source. Csv, Excel, ODF etc
"""

from pathlib import Path
from typing import List

from .table import LiveTable


class BaseInput:
    """
    A class representing source input representing more than one table
    """

    def __init__(
        self,
        had_initial_path: Path = None,
        tables: List[LiveTable] = None,
    ):
        self.had_initial_path = had_initial_path
        self.tables = tables

    def __iter__(self):
        """
        Iterate tables, use a generator to try and save a little memory.
        """
        for table in self.tables:
            yield table
