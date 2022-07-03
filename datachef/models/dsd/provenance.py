from dataclasses import dataclass
from typing import List, Optional


@dataclass
class InputProvenance:
    """
    A class to represent and track provenance information about
    a given data source being transformed.
    """

    ...


@dataclass
class OutputProvenance:
    """
    Provenance metadata about the new output we are creating, contains
    per input provenence information.
    """

    input_sources: List[InputProvenance]
    ...
