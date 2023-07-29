from __future__ import annotations

import copy
from typing import Callable, Dict, List, Optional

from tidychef.column.base import BaseColumn
from tidychef.exceptions import CellValidationError
from tidychef.lookup.base import BaseLookupEngine
from tidychef.lookup.engines.constant import Constant
from tidychef.lookup.engines.horizontal_condition import HorizontalCondition
from tidychef.models.source.cell import Cell


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

    _table: Optional[str] = "Unnamed Table"
    _apply_cache: Optional[Dict[Cell, Cell]] = None
    _validated_cells: Optional[List[Cell]] = None

    @property
    def table(self) -> str:
        """
        Returns table name where table name is known,
        else "Unnamed Table"
        """
        return self._table

    @staticmethod
    def horizontal_condition(
        column_label: str, resolver: Callable, priority=0
    ) -> Column:
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
    def constant(column_label: str, constant: str) -> Column:
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
        Things to be applied before the bulk of the BaseColumn
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
            self._apply_cache = {}

        # ----------
        # Validation
        # ----------
        self.validation = kwargs.get("validate", None)
        if self.validation:
            assert callable(
                self.validation
            ), "Value of Kwarg 'validation' must be a python callable"
            self._validated_cells = []

    def _post_lookup(self, cell: Cell) -> Cell:
        """
        Makes use of apply and/or validation callables where the
        user has provided them.

        :param cell: A single instance of a tidychef Cell object.
        :return: A single instance of a tidychef Cell object.
        """

        # Apply
        # -----
        # We need to be careful not to change the Cell itself
        # as it might be called by other Columns.
        # Instead we:
        # (1) copy before modifying
        # (2) cache, so we only have to apply once per unique
        # input value (each column cell can resolve for many
        # observations)
        if self.apply is not None:
            already_applied_cell = self._apply_cache.get(cell.value, None)
            if already_applied_cell is None:
                applied_cell = copy.deepcopy(cell)
                applied_cell.value = self.apply(applied_cell.value)
                self._apply_cache[cell.value] = applied_cell
                cell = applied_cell
            else:
                cell = already_applied_cell

        # Validate
        # --------
        # Any _unique_ Cell value is either valid in this context or it
        # isn't, so only check its valid once.
        if self.validation is not None and cell not in self._validated_cells:
            self._validated_cells.append(cell)
            if not self.validation(cell):
                if hasattr(self.validation, "msg"):
                    msg = f"Message is: {self.validation.msg(cell)}"
                else:
                    msg = ""
                raise CellValidationError(
                    f"""
                        Column {self.label} has a cell that is not valid,
                        Invalid cell {cell}.
                        {msg}                      
                        """
                )

        return cell
