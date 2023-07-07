import shutil
from pathlib import Path
from typing import List

import pytest
import requests
from pytest_mock import mocker

from datachef import acquire
from datachef.selection.xlsx.xlsx import XlsxSelectable


def test_xlsx_via_http():
    """
    Test that we can get a simple xlsx via http
    """

    selections: List[XlsxSelectable] = acquire.xlsx.http(
        "https://raw.githubusercontent.com/mikeAdamss/"
        "datachef/main/tests/fixtures/xlsx/ons-oic.xlsx"
    )
    selection = selections[3]

    assert selection.excel_ref("A7").lone_value() == "1997"
    assert selection.excel_ref("C14").lone_value() == "70.2"


def test_xlsx_url_validator():
    """
    Test that urls passed in ae validated as being
    urls
    """

    # Should not work
    with pytest.raises(AssertionError):
        acquire.xlsx.http("foo")


def test_xls_http_exception(mocker):
    """
    For non 2xx responses a http error is raised.
    """

    mock_response = mocker.Mock()
    mock_response.ok = False

    mock_session = mocker.Mock()
    mock_session.get = lambda x: mock_response

    with pytest.raises(requests.exceptions.HTTPError):
        acquire.xlsx.http(
            "https://raw.githubusercontent.com/mikeAdamss/"
            "datachef/main/tests/fixtures/xlsx/ons-oic.xlsx",
            session=mock_session,
            cache=False,
        )


def test_xls_caching():
    """
    Test that http get caching behaviour can be toggled off.
    """

    # Remove any longering .cache
    cache_dir = Path(".cache")
    if cache_dir.exists():
        shutil.rmtree(cache_dir)

    # Run a cache-less get
    acquire.xlsx.http(
        "https://raw.githubusercontent.com/mikeAdamss/"
        "datachef/main/tests/fixtures/xlsx/ons-oic.xlsx",
        cache=False,
    )

    # Confirm no .cache directory has been created.
    cache_dir = Path(".cache")
    assert not cache_dir.exists()
