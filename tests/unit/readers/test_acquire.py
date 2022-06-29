from datachef import acquire
from datachef.selection.selectable import Selectable
from tests.fixtures import path_to_fixture


def test_acquire_local():
    """
    Test that the qcquire fuction works with a local csv
    """

    csv_path = path_to_fixture("csv", "simple-small.csv")
    assert isinstance(acquire(csv_path), Selectable)

    csv_path_as_str = csv_path.resolve()
    assert isinstance(acquire(csv_path_as_str), Selectable)
