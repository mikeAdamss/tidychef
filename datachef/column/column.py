from datachef.column.base import BaseColumn
from datachef.lookup.base import BaseLookupEngine
from datachef.models.source.cell import Cell
from datachef.selection.selectable import Selectable
from datachef.validation.base import BaseValidation


class Column(BaseColumn):
    """
    The most basic implementation of a class that represents
    something that can be resolve into a column of data.

    This class differs from BaseColumn because:

    1. It allows the overriding of the value of cells that
    are extracted via the apply=keyword

    2. It allows the validation of data extracted via
    the validation= or v= keywords.
    """

    def _pre_init(self, label: str, engine: BaseLookupEngine, *args, **kwargs):
        """ """

        # -----
        # Apply
        # -----

        apply_long_form = kwargs.get("apply", None)
        apply_short_form = kwargs.get("a", None)

        assert not (
            apply_long_form and apply_short_form
        ), "Either specify validation with validation= or v= , not both."

        if apply_long_form:
            self.apply = apply_long_form
        elif apply_short_form:
            self.apply = apply_short_form
        else:
            self.apply = None

        if self.apply:
            assert callable(
                self.apply
            ), "Value of Kwarg 'apply' must be a python callable"

        # ----------
        # Validation
        # ----------

        validation_long_form = kwargs.get("validation", None)
        validation_short_form = kwargs.get("v", None)

        assert not (
            validation_long_form and validation_short_form
        ), "Either specify validation with validation= or v= , not both."

        if validation_short_form:
            self.validation = validation_short_form
        elif validation_long_form:
            self.validation = validation_long_form
        else:
            self.validation = None

    def _post_lookup(self, cell: Cell):
        """
        If someone has passed in a callable with the apply= keyword,
        the apply said callable to any cell found for this column before
        returning it
        """

        # Apply any modifications
        if self.apply:
            cell.value = self.apply(cell.value)

        # Validate
        if self.validation:
            self.validation(cell)

        return cell
