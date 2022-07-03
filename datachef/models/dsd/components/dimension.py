from abc import ABCMeta
from dataclasses import dataclass
from os import linesep
from typing import Any, List, Optional

from datachef.exceptions import BadDimensionConstructor, ComponentConstructionError
from datachef.lookup.base import BaseLookupEngine
from datachef.models.source.cell import Cell
from datachef.selection.selectable import Selectable

from .base import BaseComponent


@dataclass
class DimensionConstant:
    """
    A dimension representing a constant value
    """


@dataclass
class DimesionType:
    """
    Helper to hold simple patterns of arg types and
    kwargs for identifying the required dimension
    sub class
    """

    dim_type: DimensionConstant
    arg_types: List[Any]
    required_kwargs: List[str]
    description: str

    def __repr__(self):
        """
        A sensible string representation of this style of dimension
        to inform user feedback.
        """
        return f"{type(self.dim_type)}{linesep}{self.description}"


@dataclass
class DimensionConstant:
    """
    A dimension representing a constant value
    """


class Dimension(BaseComponent):
    """
    A component representing a dimension.
    """

    selection: Optional[Selectable]
    relational_engine: Optional[BaseLookupEngine]
    engine_param1: Optional[Any]
    engine_param2: Optional[Any]
    constant: Optional[str]
    property_url: Optional[str]

    def _post_init(self, *args, **kwargs):
        """
        Initialise this component as a dimension
        """

        # Identify purpose and behaviour based on parameters supplied
        allowed_dimension_types = {
            DimesionType(
                dim_type=DimensionConstant,
                arg_types=[Selectable],
                required_kwargs=["constant"],
                description=(
                    "A constant dimension, defined by passing a dimensions "
                    "name follow by the constant keyword. For example:{linesep}"
                    'Dimension("my dimension just contains foo", constant="foo")"'
                ),
            )
        }

        dim_type: Dimension = None
        for dimension_type in allowed_dimension_types:

            # do we have the expected number of arguments
            if len(*args) != len(dimension_type.arg_types):
                continue

            if len(**kwargs) != len(dimension_type.required_kwargs):
                continue

            for i, arg in enumerate(args):
                if not isinstance(arg, dimension_type.arg_types[i]):
                    continue

            for kwarg in kwargs:
                if kwarg not in kwargs:
                    continue

            dim_type = dimension_type
            break

        else:
            raise BadDimensionConstructor(
                "Unable to identify dimension type, must be on of: {linesep}"
                f"{linesep.join(allowed_dimension_types)}"
            )


@dataclass
class DimensionConstant:
    """
    A dimension representing a constant value
    """
