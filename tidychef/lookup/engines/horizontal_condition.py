from typing import Callable, Dict

from tidychef.exceptions import (
    BadConditionalResolverError,
    HorizontalConditionalHeaderError,
)
from tidychef.models.source.cell import Cell, VirtualCell

from ..base import BaseLookupEngine


class HorizontalCondition(BaseLookupEngine):
    """
    A lookup engine to populate the contents of a column based
    on the values resolved for the other columns on the row.
    """

    def __init__(
        self,
        label: str,
        resolver: Callable[[Dict[str, str]], str],
        priority: int = 0,
        table: str = "Unnamed Table",
    ):
        """
        A lookup engine to populate the contents of a column based
        on the values resolved for the other columns on the row.

        :param label: The label of the column informed
        by this lookup engine.
        :param resolver: The callable that will create the new column value
        :param priority: The priority used when resolving multiple horizontal
        conditions, 0 is highest priority and the default.
        :param table: the name of the table data is being extracted from
        """
        self.label = label
        self.resolver = resolver
        self.priority = priority
        self.table = table

    def resolve(self, _: Cell, cells_on_row: Dict[str, str]) -> VirtualCell:
        """
        For a given observation row (as denoted by the unused Cell argument),
        resolve the

        :param _: Unused tidychef cell object representing the observation in
        question. Required to match api signature used by other look engines.
        :param cells_on_row: Dictionary containing contents of other
        columns already resolve against the observation cell.
        :return: The value for the column.
        """

        if not isinstance(cells_on_row, dict):
            raise BadConditionalResolverError(
                f"""
                Issue encountered when processing table: "{self.table}".

                A condition resolver should take an argument of type:
                Dict[str, str] and return type str.
                                              
                The resolver for {self.label} is incorrect, it has
                input_type: {type(cells_on_row)}
                """
            )

        try:
            column_value = self.resolver(cells_on_row)
            if not isinstance(column_value, str):
                raise BadConditionalResolverError(
                    f"""
                    Issue encountered when processing table: "{self.table}".

                    A condition resolver should take an argument of type:
                    Dict[str, str] and return type str.
                                                    
                    The resolver for {self.label} is incorrect, it has:

                    return type: {type(column_value)}
                    return value: {column_value} 
                    """
                )
            return VirtualCell(value=column_value)

        except KeyError as err:
            raise HorizontalConditionalHeaderError(
                f"""
                Issue encountered when processing table: "{self.table}".

                Unable to resolve lookup for "{self.label}".
                                               
                The column header key "{err.args[0]}" was specified in:
                the condition but is not (yet?) present on the resolved row:
                
                Header Keys: {cells_on_row.keys()}

                Note - please be aware of ordering when using horizontal conditions
                that interact (i.e where condition 2 required condition 1 to be
                resolved first)

                The priority= keyword can be used with the Column.horizontal_condition()
                constructor where conditionals must be sequenced. The lower the priority
                the sooner the condition is executed.
                """
            ) from err
        except Exception as err:
            raise err
