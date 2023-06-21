import os
from pathlib import Path

import pytest

from datachef.exceptions import OutputPassedToPreview, UnalignedTableOperation
from datachef.notebook.preview.html.main import preview
from datachef.output.tidydata import TidyData
from datachef.selection.selectable import Selectable
from tests.fixtures.helpers import path_to_fixture
from tests.fixtures.preconfigured import fixture_simple_small_one_tab


@pytest.fixture
def selectable_simple_small1():
    return fixture_simple_small_one_tab()


@pytest.fixture
def selectable_simple_small2():
    return fixture_simple_small_one_tab()


def test_preview_is_callable(selectable_simple_small1: Selectable):
    """
    Confirm sure that the preview callable can be called with
    a variable number of selections, i.e *args but only of
    type Selectable.
    """

    s1 = selectable_simple_small1.excel_ref("C6:E7")
    s2 = selectable_simple_small1.excel_ref("A2:A10")
    s3 = selectable_simple_small1.excel_ref("G4:H4")
    s4 = selectable_simple_small1.excel_ref("G4:H4")
    s5 = selectable_simple_small1.excel_ref("G4:H4")

    preview(s1)
    preview(s1, s2, s3)
    preview(s1, s2, s3, s4, s5)

    with pytest.raises(AssertionError):
        preview(s1, s2, s3, True)

    with pytest.raises(AssertionError):
        preview([], s1)

    with pytest.raises(AssertionError):
        preview(s1, s2, None, s4, s5)


def test_previwer_with_mixed_table_raises(
    selectable_simple_small1: Selectable, selectable_simple_small2: Selectable
):
    """
    Confirm that where a user tries to create a preview with selections
    from two different data sources, a suitable exception is raised.
    """

    with pytest.raises(UnalignedTableOperation):
        preview(selectable_simple_small1, selectable_simple_small2)


def test_passing_an_output_to_preview_raises(selectable_simple_small1: Selectable):
    """
    Test that where users have tried to pass an output
    class to the input preview the expected error is
    raised.
    """

    with pytest.raises(OutputPassedToPreview):
        # Note, empty args as its just checking the type
        # not the contents and should fail immediately
        preview(
            TidyData(
                selectable_simple_small1.label_as("foo"),
                [selectable_simple_small1.label_as("foo")],
            )
        )


def test_output_preview_to_path_works(selectable_simple_small1: Selectable):
    """
    Test that the ability to output the html preview to
    a path works.
    """

    here = Path(__file__).parent
    test_output_path = Path(here / "deleteme.html")

    preview(selectable_simple_small1, path=test_output_path)
    with open(test_output_path) as f:
        new_content = f.read()
    os.remove(test_output_path)

    html_fixture = path_to_fixture("preview", "simple-output.html")
    with open(html_fixture) as f:
        fixture_content = f.read()

    assert new_content == fixture_content
