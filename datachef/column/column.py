from datachef.column.base import BaseColumn
from datachef.lookup.base import BaseLookupEngine
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

    def _pre_init(self, label: str, engine: BaseLookupEngine, *args, **kwargs):
        """ """

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

        # TODO - list of callables?
        self.validation = kwargs.get("validation", None)
        if self.validation:
            assert callable(
                self.validation
            ), "Value of Kwarg 'validation' must be a python callable"

    def _post_lookup(self, cell: Cell):
        """
        Makes use of apply and/or validation callables where the
        user has provided them.
        """

        # Apply any modifications
        if self.apply:
            cell.value = self.apply(cell.value)

        # Validate
        if self.validation:
            self.validation(cell)

        return cell
