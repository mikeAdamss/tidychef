from dataclasses import dataclass

from datachef.exceptions import (
    BadDimensionConstructor,
    CellsDoNotExistError,
    ComponentConstructionError,
    FailedLookupError,
    MissingDirectLookupError,
    UnknownDirectionError,
    UnnamedTableError,
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
        Case(ComponentConstructionError, "Invalid parameters supplied to constructor."),
        Case(UnknownDirectionError, "Direction is not a valid direction."),
        Case(
            MissingDirectLookupError,
            "Cannot use a direct lookup, no value found in the direction specified.",
        ),
        Case(
            FailedLookupError, "Lookup has failed, no relative cell could be resolved."
        ),
        Case(
            BadDimensionConstructor,
            "Cannot construct dimension, an unrecognised combination of parameters has been supplied.",
        ),
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
