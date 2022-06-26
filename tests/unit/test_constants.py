from datachef.constants import SupportedLocalFiles


def test_local_filetype_repr():
    """
    Test our local filetype __repr__ functionality works
    as intended.
    """
    assert str(SupportedLocalFiles()) == "csv"
