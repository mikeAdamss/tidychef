from abc import ABCMeta

from tidychef.lookup.base import BaseLookupEngine
from tidychef.models.source.cell import Cell


class BaseColumn(metaclass=ABCMeta):
    """
    A base class to hold the required variables for something
    that can be resolve to a column of data.
    """

    def __init__(
        self,
        engine: BaseLookupEngine,
        *args,
        **kwargs,
    ):
        """
        An object representing a proto column that can resolve a
        visual relationship to retrieve the appropriate column
        value relative to a given observation containing cell object.

        :param engine: The "lookup engine" that resolves cell value lookups.
        """

        # See _pre_init() docstring
        self._pre_init(self, engine, *args, **kwargs)

        assert isinstance(
            engine, BaseLookupEngine
        ), f"""
                {engine} is not a valid argument.
                
                Argument must be of type BaseLookupEngine.
        """

        self.engine = engine
        self.label = engine.label

        # See _post_init() docstring
        self._post_init(self, engine, *args, **kwargs)

    def _pre_init(
        self,
        engine: BaseLookupEngine,
        *args,
        **kwargs,
    ):
        """
        Overridable method for doing something clever just before the bulk
        of the __init__ logic is executed.

        :param engine: The "lookup engine" that resolves cell value lookups.
        """
        ...

    def _post_init(
        self,
        engine: BaseLookupEngine,
        *args,
        **kwargs,
    ):
        """
        Overridable method for doing something clever just after the __init__
        logic is executed.

        :param engine: The "lookup engine" that resolves cell value lookups.
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

        :param cell: A single tidychef Cell object.
        :return: A single tidychef Cell object.
        """
        return cell

    def resolve_column_cell_from_obs_cell(self, observation_cell: Cell, *args) -> Cell:
        """
        Use the provided lookup engine to return the value
        of this Column against a given observation, according
        to the lookup engine in use.

        The found cell is ran through _post_lookup() in case
        this particular Column is applying custom handling of
        some sort.

        :param cell: A single tidychef Cell object.
        :return: A single tidychef Cell object.
        """
        cell = self.engine.resolve(observation_cell, *args)
        cell = self._post_lookup(cell)
        return cell
