"""
Classes representing a single input.

An input would be a single tabulated source. Csv, Excel, ODF or the in memory
representation of same (to include dataframes).
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List

import pivoter.models.source


@dataclass
class Input:
    """
    A class representing a single input (typically a file)
    """
    is_singelton_table: bool
    selected_table: pivoter.models.source.LiveTable

    had_initial_path: Optional[Path]
    tables: Optional[List[pivoter.models.source.LiveTable]]
