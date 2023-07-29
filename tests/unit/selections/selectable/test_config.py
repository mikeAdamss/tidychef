from pathlib import Path

import pytest

from tests.fixtures import fixture_simple_one_tab
from tidychef.selection.selectable import Selectable


@pytest.fixture
def selectable_simple1():
    return fixture_simple_one_tab()


def test_selectable_config(selectable_simple1: Selectable):
    """
    Test the config setting method works as expected.
    """

    assert selectable_simple1._explain is False
    selection = selectable_simple1.config(explain=True)
    assert selection._explain is True

    assert selectable_simple1._explain_path is None
    selection = selectable_simple1.config(explain_path="foo")
    assert selection._explain_path == Path("foo")
