from pathlib import Path
from typing import List

from tidychef import acquire
from tidychef.selection.xlsx.xlsx import XlsxSelectable
from tests.fixtures import path_to_fixture


def test_acquire_local_xls():
    """
    Test that the acquire function works with a local xls
    """

    xlsx_path = path_to_fixture("xlsx", "ons-oic.xlsx")
    assert isinstance(acquire.xlsx.local(xlsx_path)[0], XlsxSelectable)

    xlsx_path_as_str = xlsx_path.resolve()
    assert isinstance(acquire.xlsx.local(xlsx_path_as_str)[0], XlsxSelectable)


def test_read_local_xls_from_path():
    """
    Test local file loader for xls from path
    """
    xlsx_path: Path = path_to_fixture("xlsx", "ons-oic.xlsx")
    sheets: List[XlsxSelectable] = acquire.xlsx.local(xlsx_path)
    sheet = sheets[3]

    assert sheet.cells == sheet.pcells
    assert len(sheet.cells) == 4455


def test_read_local_xls_from_str():
    """
    Test local file loader for csv from str
    """
    xlsx_path: Path = path_to_fixture("xlsx", "ons-oic.xlsx")
    sheets: List[XlsxSelectable] = acquire.xlsx.local(str(xlsx_path.absolute()))
    sheet = sheets[3]

    assert sheet.cells == sheet.pcells
    assert len(sheet.cells) == 4455
