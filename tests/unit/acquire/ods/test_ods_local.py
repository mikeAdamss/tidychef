from pathlib import Path
from typing import List

from tests.fixtures import path_to_fixture
from tidychef import acquire
from tidychef.selection.ods.ods import OdsSelectable


def test_acquire_local_ods():
    """
    Test that the acquire function works with a local ods
    """

    ods_path = path_to_fixture("ods", "bands-wide.ods")
    assert isinstance(acquire.ods.local(ods_path)[0], OdsSelectable)

    ods_path_as_str = ods_path.resolve()
    assert isinstance(acquire.ods.local(ods_path_as_str)[0], OdsSelectable)


def test_read_local_ods_from_path():
    """
    Test local file loader for ods from path
    """
    ods_path: Path = path_to_fixture("ods", "bands-wide.ods")
    sheets: List[OdsSelectable] = acquire.ods.local(ods_path)
    sheet = sheets[0]

    assert sheet.cells == sheet.pcells
    assert len(sheet.cells) == 77


def test_read_local_ods_from_str():
    """
    Test local file loader for ods from str
    """
    ods_path: Path = path_to_fixture("ods", "bands-wide.ods")
    sheets: List[OdsSelectable] = acquire.ods.local(str(ods_path.absolute()))
    sheet = sheets[0]

    assert sheet.cells == sheet.pcells
    assert len(sheet.cells) == 77


def test_ods_local_time_format():
    """
    Test that the ods time_format keyword works as expected.
    """

    xls_path: Path = path_to_fixture("ods", "dates-times.ods")
    sheet: OdsSelectable = acquire.ods.local(str(xls_path.absolute()), tables="Sheet1")
    assert [x.value for x in sheet.pcells] == [
        "dates",
        "11/01/23",
        "11/01/23",
        "12/01/22",
        "10/10/00",
    ]
