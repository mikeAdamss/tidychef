from pathlib import Path

import pytest
import requests
from pytest_mock import mocker

from datachef import acquire
from datachef.selection.selectable import Selectable


def test_csv_via_http():
    """
    Test that we can get a simple csv via http
    """

    selection: Selectable = acquire.csv.http(
        "https://raw.githubusercontent.com/mikeAdamss/"
        "datachef/main/tests/fixtures/csv/bands.csv"
    )
    assert selection.excel_ref("C2").lone_value() == "Houses"
    assert selection.excel_ref("B7").lone_value() == "Ringo"


def test_url_validator():
    """
    Test that urls passed in ae validated as being
    urls
    """

    # Should not work
    with pytest.raises(AssertionError):
        acquire.csv.http("foo")


def test_http_exception(mocker):
    """
    For non 2xx responses a http error is raised.
    """

    mock_response = mocker.Mock()
    mock_response.ok = False

    mock_session = mocker.Mock()
    mock_session.get = lambda x: mock_response

    with pytest.raises(requests.exceptions.HTTPError):
        acquire.csv.http(
            "https://raw.githubusercontent.com/mikeAdamss/"
            "datachef/main/tests/fixtures/csv/bands.csv",
            session=mock_session,
        )
