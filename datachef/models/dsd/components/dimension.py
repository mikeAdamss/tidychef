from dataclasses import dataclass
from typing import List, Optional

from datachef.models.source.cell import Cell

from .base import BaseComponent


@dataclass
class Dimension(BaseComponent):
    """
    A component representing a dimension.
    """

    property_url: Optional[str]
