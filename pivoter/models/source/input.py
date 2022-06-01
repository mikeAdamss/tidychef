"""
Classes representing a single input.

An input would be a single tabulated source. Csv, Excel, ODF or the in memory
representation of same (to include dataframes).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List

from .table import LiveTable, Table


@dataclass
class Input:
    """
    A class representing a single input (typically though not exclusively a file)
    """

    is_singelton_table: bool
    selected_table: LiveTable

    had_initial_path: Optional[Path]
    tables: Optional[List[LiveTable]]

    def from_single_table(file_path: Path, table: Table) -> Input:
        """
        Construct an Input object from a single table
        """
        return Input(
            is_singelton_table = True,
            selected_table = LiveTable.from_table(name=file_path.name, table=table),
            had_initial_path = file_path,
            tables = None
        )
