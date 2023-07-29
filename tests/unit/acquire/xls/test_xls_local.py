from pathlib import Path
from typing import List

import pytest
from pytest_mock import mocker

from tests.fixtures import path_to_fixture
from tidychef import acquire
from tidychef.selection.xls.xls import XlsSelectable


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


def test_shared_xls_local_time_formatting_works():
    """
    Test that the xls time_format keyword works as expected.
    """

    xls_path: Path = path_to_fixture("xls", "dates-times.xls")
    sheet: XlsSelectable = acquire.xls.local(xls_path, tables="Sheet1")
    assert [x.value for x in sheet.pcells] == [
        "dates",
        "11/01/23",
        "11/01/23",
        "12/01/22",
        "10/10/00",
    ]


def test_unknown_xls_local_time_format_can_be_specified(mocker):
    """
    Test that were we don't have knowledge of an xls time
    format string the user can explicitly pass in a
    formatting string.
    """

    mocker.patch("tidychef.acquire.xls.shared.xls_time_formats", return_value={})

    xls_path: Path = path_to_fixture("xls", "dates-times.xls")
    sheet: XlsSelectable = acquire.xls.local(
        xls_path, tables="Sheet1", custom_time_formats={"DD/MM/YY": "%d/%m/%y"}
    )

    assert [x.value for x in sheet.pcells] == [
        "dates",
        "11/01/23",
        "11/01/23",
        "12/01/22",
        "10/10/00",
    ]
