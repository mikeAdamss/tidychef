from pathlib import Path
from typing import List

from tests.fixtures import path_to_fixture
from tidychef import acquire
from tidychef.selection.xlsx.xlsx import XlsxSelectable


def test_acquire_local_xlsx():
    """
    Test that the acquire function works with a local xls
    """

    xlsx_path = path_to_fixture("xlsx", "ons-oic.xlsx")
    assert isinstance(acquire.xlsx.local(xlsx_path)[0], XlsxSelectable)

    xlsx_path_as_str = xlsx_path.resolve()
    assert isinstance(acquire.xlsx.local(xlsx_path_as_str)[0], XlsxSelectable)


def test_read_local_xlsx_from_path():
    """
    Test local file loader for xls from path
    """
    xlsx_path: Path = path_to_fixture("xlsx", "ons-oic.xlsx")
    sheets: List[XlsxSelectable] = acquire.xlsx.local(xlsx_path)
    sheet = sheets[3]

    assert sheet.cells == sheet.pcells
    assert len(sheet.cells) == 4455


def test_read_local_xlsx_from_str():
    """
    Test local file loader for csv from str
    """
    xlsx_path: Path = path_to_fixture("xlsx", "ons-oic.xlsx")
    sheets: List[XlsxSelectable] = acquire.xlsx.local(str(xlsx_path.absolute()))
    sheet = sheets[3]

    assert sheet.cells == sheet.pcells
    assert len(sheet.cells) == 4455

def test_unknown_xlsx_local_time_format_can_be_specified(mocker):
    """
    Test that were we don't have knowledge of an xlsx time
    format string the user can explicitly pass in a
    formatting string.
    """

    mocker.patch("tidychef.acquire.xlsx.shared.xlsx_time_formats", return_value={})

    xlsx_path: Path = path_to_fixture("xlsx", "dates-times.xlsx")
    sheet: XlsxSelectable = acquire.xlsx.local(xlsx_path, tables="Sheet1",
        custom_time_formats={"d/m/yyyy": "%d/%m/%y"},
    )

    assert [x.value for x in sheet.pcells] == [
        "dates",
        "11/01/23",
        "11/01/23",
        "12/01/22",
        "10/10/00",
        "",
    ]