"""
Classes representing a single cell of data.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

import pivoter.models.source
import pivoter.exceptions

@dataclass
class Table:
    cells: List[pivoter.models.source.Cell]
    name: Optional[str]

    @property
    def title(self):
        """
        Alternative accessor for table.name.
        Returns a name if we have a name, else raises
        """
        return self.name()

    @property
    def name(self):
        """
        Return a name if we have a name, else raises
        """
        if self.name:
            return self.name
        else:
            raise pivoter.exceptions.UnnamedTableError

@dataclass
class LiveTable:
    """
    A "live" table represents two things:

    1.) "printine" - The pristine table as pulled from the source.
    2.) "filtered" - The current subset of cells as selected from the pristine table.

    Keeping track of the pristine cell selection (the initial table) allows us to
    extend a Table of cells (.filtered) via comparing it with the pristine Table
    (.pristine). This enables the extension of a cell selection as well as the
    filtering down of one.
    """
    pristine: Table
    filtered: Table
    
    @staticmethod
    def from_table(table: Table) -> LiveTable:
        return LiveTable(
            pristine = table,
            filtered = table
        )
