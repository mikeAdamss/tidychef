from typing import Callable

from datachef.column.base import BaseColumn
from datachef.lookup.base import BaseLookupEngine
from datachef.lookup.engines.constant import Constant
from datachef.lookup.engines.horizontal_condition import HorizontalCondition
from datachef.models.source.cell import Cell


class Column(BaseColumn):
    """
    A basic implementation of a class that represents
    something that can be resolve into a column of data.

    This class differs from BaseColumn because:

    1. It allows the overriding of the value of cells that
    are extracted via the apply=keyword

    2. It allows the validation of data extracted via
    the validation= keyword.
    """

    @staticmethod
    def horizontal_condition(column_label: str, resolver: Callable, priority=0):
        """
        Creates a column that populates based on the
        values resolved for one or more other columns.

        :param column_label: The label we wish to give to the column.
        :param resolver: A callable to resolve the horizontal condition logic.
        :priority: controls order of resolution for all present HorizontalCondition objects,
        lower values are resolved first.
        :return: A Column object populated with a configured HorizontalCondition
        lookup engine.
        """
        return Column(HorizontalCondition(column_label, resolver, priority=priority))

    @staticmethod
    def constant(column_label: str, constant: str):
        """
        Create a column that has one specific value for every
        entry.

        :param column_label: The label we wish to give to the column.
        :param constant: The constant value we wish to populate the column.
        :return: A Column object populated with a configured Constant lookup engine.
        """
        return Column(Constant(column_label, constant))

    def _pre_init(self, engine: BaseLookupEngine, *args, **kwargs):
        """
        Things to be applied before the bulk of the BaeColumn
        init logic.

        :engine: The lookup engine in use by this column.
        """
        
        # -----
        # Apply
        # -----
        self.apply = kwargs.get("apply", None)
        if self.apply:
            assert callable(
                self.apply
            ), "Value of Kwarg 'apply' must be a python callable"

        # ----------
        # Validation
        # ----------
        self.validation = kwargs.get("validate", None)
        if self.validation:
            assert callable(
                self.validation
            ), "Value of Kwarg 'validation' must be a python callable"

    def _post_lookup(self, cell: Cell) -> Cell:
        """
        Makes use of apply and/or validation callables where the
        user has provided them.

        :param cell: A single instance of a datachef Cell object.
        :return: A single instance of a datachef Cell object.
        """

        # Apply any modifications
        if self.apply:
            cell.value = self.apply(cell.value)

        # Validate
        if self.validation:
            self.validation(cell)

        return cell
