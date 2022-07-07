from dataclasses import dataclass

from datachef.exceptions import (
    DimensionConstructionError,
    CellsDoNotExistError,
    NonExistentCellComparissonError,
    FailedLookupError,
    MissingDirectLookupError,
    UnknownDirectionError,
    UnnamedTableError,
    InvlaidCellPositionError
)


def test_exception_defaults_can_be_overwritten():
    """
    Test that our exceptions have default text but that
    text can be overwritten
    """

    override_msg = "foo bar baz"

    @dataclass
    class Case:
        exception: Exception
        default_msg: str

    for case in [
        Case(CellsDoNotExistError, "Requested cells are not in current selection"),
        Case(
            UnnamedTableError,
            "Cannot access table name/title property as this table does not have one.",
        ),
        Case(UnknownDirectionError, "Direction is not a valid direction."),
        Case(
            MissingDirectLookupError,
            "Cannot use a direct lookup, no value found in the direction specified.",
        ),
        Case(
            FailedLookupError, "Lookup has failed, no relative cell could be resolved."
        ),
        Case(
            DimensionConstructionError,
            "Cannot construct dimension, an unrecognised combination of parameters has been supplied.",
        ),
        Case(
            NonExistentCellComparissonError,
            "You cannot make a postitional comparisson between a cell parsed from a source input and a virtual cell."
        ),
        Case(
            InvlaidCellPositionError,
            "A cell with any postional values must exist on both the x and y axis."
        )
    ]:

        # Assert initially as expected
        default_err = case.exception()
        default_err_str = str(default_err)
        assert case.default_msg in default_err_str, (
            "Error {case.exception} does not contain expected err message: ",
            f'"{case.default_msg}", instead we got: "{default_err_str}"',
        )

        # Assert override as expected
        overwritten_err = case.exception(override_msg)
        overwritten_err_str = str(overwritten_err)
        assert override_msg in overwritten_err_str, (
            "Error {case.exception} does not contain the provided err message: ",
            f'"{override_msg}", instead we got: "{overwritten_err_str}"',
        )
