"""
Classes representing a sinlge cell of data.
"""

from dataclasses import dataclass
from typing import Optional

import pivoter.models.source


@dataclass
class Cell:
    x: int
    y: int
    cellformat: Optional[pivoter.models.source.CellFormatting]
