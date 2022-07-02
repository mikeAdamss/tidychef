from datachef.exceptions import CellsDoNotExistError, UnnamedTableError

from dataclasses import dataclass

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
        Case(UnnamedTableError, "Cannot access table name/title property as this table does not have one.")
        ]:


        # Assert initially as expected
        default_err = case.exception()
        default_err_str = str(default_err)
        assert case.default_msg in default_err_str, (
            'Error {case.exception} does not contain expected err message: ',
            f'"{case.default_msg}", instead we got: "{default_err_str}"'
        )

        # Assert override as expected
        overwritten_err = case.exception(override_msg)
        overwritten_err_str = str(overwritten_err)
        assert override_msg in overwritten_err_str, (
            'Error {case.exception} does not contain the provided err message: ',
            f'"{override_msg}", instead we got: "{overwritten_err_str}"'
        )
