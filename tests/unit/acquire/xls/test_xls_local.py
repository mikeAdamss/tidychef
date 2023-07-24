from pathlib import Path
from typing import List

from tidychef import acquire
from tidychef.selection.xls.xls import XlsSelectable
from tests.fixtures import path_to_fixture


def test_acquire_local_xls():
    """
    Test that the acquire function works with a local xls
    """

    xls_path = path_to_fixture("xls", "sample.xls")
    assert isinstance(acquire.xls.local(xls_path)[0], XlsSelectable)

    xls_path_as_str = xls_path.resolve()
    assert isinstance(acquire.xls.local(xls_path_as_str)[0], XlsSelectable)


def test_read_local_xls_from_path():
    """
    Test local file loader for xls from path
    """
    xls_path: Path = path_to_fixture("xls", "sample.xls")
    sheets: List[XlsSelectable] = acquire.xls.local(xls_path)
    sheet = sheets[0]

    assert sheet.cells == sheet.pcells
    assert len(sheet.cells) == 51


def test_read_local_xls_from_str():
    """
    Test local file loader for csv from str
    """
    xls_path: Path = path_to_fixture("xls", "sample.xls")
    sheets: List[XlsSelectable] = acquire.xls.local(str(xls_path.absolute()))
    sheet = sheets[0]

    assert sheet.cells == sheet.pcells
    assert len(sheet.cells) == 51
