"""
Classes representing a sinlge cell of data.
"""

from dataclasses import dataclass
from typing import Optional

from .cellformat import CellFormatting

class Cell:

    def __init__(self, value: str, x: int, y: int, cell_formatting: Optional[CellFormatting] = None):
        self.value = value
        self.x: int = x
        self.y: int = y
        self.cellformat: Optional[CellFormatting] = cell_formatting
