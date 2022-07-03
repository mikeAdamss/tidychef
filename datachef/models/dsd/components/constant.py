from dataclasses import dataclass


@dataclass
class Constant:
    """
    A value and assoicated metadata that represents a constant
    value as applied to a defined component.
    """

    value: str
    data_type: str = "string"
