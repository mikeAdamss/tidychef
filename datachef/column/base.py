from abc import ABCMeta
from typing import Generator, Tuple

from datachef.lookup.base import BaseLookupEngine
from datachef.models.source.cell import Cell
from datachef.selection.selectable import Selectable


class BaseColumn(metaclass=ABCMeta):
    """
    A base class to hold the required variables for something
    that can be resolve to a column of data.
    """

    def __init__(
        self,
        label: str,
        engine: BaseLookupEngine,
        *args,
        **kwargs,
    ):
        """ """

        # Note, its not expected (nor recommended), but these booleans
        # are to allow an advanced user to toggle off the assertions
        # via _pre_init() if they're trying to do something particularly
        # whacky.
        self.assert_label = True
        self.assert_engine = True

        # See _pre_init() docstring
        self._pre_init(self, label, engine, *args, **kwargs)

        # Assert the things that we should always have
        if self.assert_label:
            assert isinstance(
                label, str
            ), f"{label} is not a valid argument. This should be of type str"

        if self.assert_engine:
            assert isinstance(
                engine, BaseLookupEngine
            ), f"{engine} is not a valid argument"  # TODO - list the options once we have them

        self.label = label
        self.engine = engine

        # See _post_init() docstring
        self._post_init(self, label, engine, *args, **kwargs)

    def _pre_init(
        self,
        label: str,
        engine: BaseLookupEngine,
        *args,
        **kwargs,
    ):
        """
        Overridable method for doing something clever just before the bulk
        of the __init__ logic is executed.
        """
        ...

    def _post_init(
        self,
        label: str,
        engine: BaseLookupEngine,
        *args,
        **kwargs,
    ):
        """
        Overridable method for doing something clever just after the __init__
        logic is executed.
        """
        ...

    def _post_lookup(self, cell: Cell):
        """
        Overridable method for doing something clever to a Cell that's just been
        resolved as belonging to this column.

        Example: prefix all cell value with "foo-"

        ```
            def _post_lookup(self, cell: Cell):
                cell.value = "foo-"+cell.value
                return Cell
        ``
        """
        return cell

    def resolve_column_cell_from_obs_cell(self, observation_cell: Cell) -> Cell:
        """
        Use the provided lookup engine to return the value
        of this Column against a given observation, according
        to the lookup engine in use.

        The found cell is ran through _post_lookup() in case
        this particular Column is applying custom handling of
        some sort.
        """
        cell = self.engine.resolve(observation_cell)
        cell = self._post_lookup(cell)
        return cell

    def lookup_preview(
        self, observation_selection: Selectable
    ) -> Generator[Tuple[Cell, Cell], None, None]:
        """
        Takes a selection of observations and generates
        tuples of:
        <observation_cell> : <column cell>

        This is intended for sanity checking during
        development, not for doing the actual transform.
        """
        for observation_cell in observation_selection.cells:
            yield observation_cell, self.resolve_column_cell_from_obs_cell(
                observation_cell
            )
