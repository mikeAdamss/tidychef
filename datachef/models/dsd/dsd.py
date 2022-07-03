from dataclasses import dataclass
from typing import List, Optional

from .components.base import BaseComponent
from .provenance import OutputProvenance


@dataclass
class DSD:

    components: List[BaseComponent]
    identifier: Optional[str]
    provenance: Optional[OutputProvenance]
