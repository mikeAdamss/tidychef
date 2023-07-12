from datachef import acquire
from datachef.selection.selectable import Selectable


def test_lists_of_lists():
    """
    Test our list of lists acquire method
    """

    selection: Selectable = acquire.python.list_of_lists(
        [["1", "2", "3"], ["4", "5", "6"]]
    )

    assert len(selection) == 6
    assert len(selection.excel_ref("A")) == 2
    assert len(selection.excel_ref("1")) == 3
