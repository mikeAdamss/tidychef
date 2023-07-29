import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import List

import pytest
import requests
from pytest_mock import mocker

from tidychef import acquire
from tidychef.selection.ods.ods import OdsSelectable


def test_ods_via_http():
    """
    Test that we can get a simple xls via http
    """

    selections: List[OdsSelectable] = acquire.ods.http(
        "https://github.com/mikeAdamss/tidychef/raw/main/tests/"
        "fixtures/ods/EB1-_Existing_Domestic_Properties.ods"
    )
    selection = selections[1]

    assert selection.excel_ref("A1").lone_value() == "Notes "


def test_ods_url_validator():
    """
    Test that urls passed in ae validated as being
    urls
    """

    # Should not work
    with pytest.raises(AssertionError):
        acquire.ods.http("foo")


def test_ods_http_exception(mocker):
    """
    For non 2xx responses a http error is raised.
    """

    mock_response = mocker.Mock()
    mock_response.ok = False

    mock_session = mocker.Mock()
    mock_session.get = lambda x: mock_response

    with pytest.raises(requests.exceptions.HTTPError):
        acquire.ods.http(
            "https://github.com/mikeAdamss/tidychef/raw/main/tests/"
            "fixtures/ods/EB1-_Existing_Domestic_Properties.ods",
            session=mock_session,
            cache=False,
        )


def test_ods_caching():
    """
    Test that http get caching behaviour can be toggled off.
    """

    # Remove any longering .cache
    cache_dir = Path(".cache")
    if cache_dir.exists():
        shutil.rmtree(cache_dir)

    # Run a cache-less get
    acquire.ods.http(
        "https://github.com/mikeAdamss/tidychef/raw/main/tests/"
        "fixtures/ods/EB1-_Existing_Domestic_Properties.ods",
        cache=False,
    )

    # Confirm no .cache directory has been created.
    cache_dir = Path(".cache")
    assert not cache_dir.exists()
