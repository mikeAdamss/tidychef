import os
from pathlib import Path
from unittest.mock import Mock

import pytest

from tests.fixtures.helpers import path_to_fixture
from tests.fixtures.preconfigured import fixture_simple_small_one_tab
from tidychef.exceptions import OutputPassedToPreview, UnalignedTableOperation
from tidychef.models.source.cellformat import CellFormatting
from tidychef.models.source.table import Table
from tidychef.notebook.preview.html.components import HtmlCell
from tidychef.notebook.preview.html.main import preview
from tidychef.output.tidydata import TidyData
from tidychef.selection.selectable import Selectable


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


def test_previewer_with_mixed_table_raises(
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


def test_multiple_selection_warnings(selectable_simple_small1: Selectable):
    """
    Test that multiple selection warnings are being shown
    as intended.
    """

    selection_one = selectable_simple_small1.excel_ref("A")
    selection_two = selectable_simple_small1.excel_ref("4")

    preview(selection_one, selection_two, path="multiple_selection_warning.html")

    with open("multiple_selection_warning.html") as f:
        preview_got = f.read()
    os.remove("multiple_selection_warning.html")

    with open(path_to_fixture("preview", "multiple_selection_warning.html")) as f:
        preview_expected = f.read()

    assert preview_got == preview_expected


def test_multiple_selection_warnings_can_be_toggled_off(
    selectable_simple_small1: Selectable,
):
    """
    Test that multiple selection warnings are being shown
    as intended.
    """

    selection_one = selectable_simple_small1.excel_ref("A")
    selection_two = selectable_simple_small1.excel_ref("4")

    preview(
        selection_one,
        selection_two,
        multiple_selection_warning=False,
        path="multiple_selection_warning_off.html",
    )

    with open("multiple_selection_warning_off.html") as f:
        preview_got = f.read()
    os.remove("multiple_selection_warning_off.html")

    with open(path_to_fixture("preview", "multiple_selection_warning_off.html")) as f:
        preview_expected = f.read()

    assert preview_got == preview_expected


def test_output_preview_to_path_works_with_no_excel_ref(
    selectable_simple_small1: Selectable,
):
    """
    Test that the ability to output the html preview to
    a path works.
    """

    here = Path(__file__).parent
    test_output_path = Path(here / "deleteme.html")

    preview(selectable_simple_small1, show_excel=False, path=test_output_path)
    with open(test_output_path) as f:
        new_content = f.read()
    os.remove(test_output_path)

    html_fixture = path_to_fixture("preview", "simple-output-no-excel-notations.html")
    with open(html_fixture) as f:
        fixture_content = f.read()

    assert new_content == fixture_content


def test_output_preview_to_path_works_with_xy_references(
    selectable_simple_small1: Selectable,
):
    """
    Test that the ability to output the html preview to
    a path works.
    """

    here = Path(__file__).parent
    test_output_path = Path(here / "deleteme.html")

    preview(
        selectable_simple_small1, show_excel=False, show_xy=True, path=test_output_path
    )
    with open(test_output_path) as f:
        new_content = f.read()
    os.remove(test_output_path)

    html_fixture = path_to_fixture("preview", "show-xy.html")
    with open(html_fixture) as f:
        fixture_content = f.read()

    assert new_content == fixture_content


def test_output_preview_to_path_works_with_both_xy_and_excel_references(
    selectable_simple_small1: Selectable,
):
    """
    Test that the ability to output the html preview to
    a path works.
    """

    here = Path(__file__).parent
    test_output_path = Path(here / "deleteme.html")

    preview(selectable_simple_small1, show_xy=True, path=test_output_path)
    with open(test_output_path) as f:
        new_content = f.read()
    os.remove(test_output_path)

    html_fixture = path_to_fixture("preview", "show-xy-and-excel.html")
    with open(html_fixture) as f:
        fixture_content = f.read()

    assert new_content == fixture_content


def test_html_cell_formatting():
    """
    Test that HtmlCell correctly applies text formatting based on CellFormatting.
    """
    from tidychef.models.source.cell import Cell
    
    # Test bold formatting
    bold_cell = Cell(value="Bold Text", x=0, y=0, cellformat=CellFormatting(bold=True))
    html_cell = HtmlCell(bold_cell, "white")
    html_output = html_cell.as_html()
    assert "<strong>Bold Text</strong>" in html_output
    assert 'style="background-color:white"' in html_output

    # Test italic formatting
    italic_cell = Cell(value="Italic Text", x=0, y=0, cellformat=CellFormatting(italic=True))
    html_cell = HtmlCell(italic_cell, "lightgrey")
    html_output = html_cell.as_html()
    assert "<em>Italic Text</em>" in html_output

    # Test underline formatting
    underline_cell = Cell(value="Underlined Text", x=0, y=0, cellformat=CellFormatting(underline=True))
    html_cell = HtmlCell(underline_cell, "cyan")
    html_output = html_cell.as_html()
    assert "<u>Underlined Text</u>" in html_output

    # Test hyperlink formatting (should override underline)
    hyperlink_cell = Cell(value="Link Text", x=0, y=0, cellformat=CellFormatting(hyperlink=True, underline=True))
    html_cell = HtmlCell(hyperlink_cell, "cyan")
    html_output = html_cell.as_html()
    assert '<span style="color: blue; text-decoration: underline;">Link Text</span>' in html_output
    assert "<u>" not in html_output  # Should NOT have <u> tags since it's a hyperlink

    # Test combined formatting
    combined_cell = Cell(value="Combined", x=0, y=0, cellformat=CellFormatting(bold=True, italic=True, underline=True))
    html_cell = HtmlCell(combined_cell, "white")
    html_output = html_cell.as_html()
    # The tags are applied in the order they appear in the code: bold, italic, underline
    assert "<u><em><strong>Combined</strong></em></u>" in html_output

    # Test hyperlink with other formatting
    hyperlink_bold_cell = Cell(value="Bold Link", x=0, y=0, cellformat=CellFormatting(hyperlink=True, bold=True, underline=True))
    html_cell = HtmlCell(hyperlink_bold_cell, "white")
    html_output = html_cell.as_html()
    assert '<strong><span style="color: blue; text-decoration: underline;">Bold Link</span></strong>' in html_output
    assert "<u>" not in html_output  # Should NOT have <u> tags since it's a hyperlink

    # Test no formatting
    plain_cell = Cell(value="Plain Text", x=0, y=0, cellformat=CellFormatting())
    html_cell = HtmlCell(plain_cell, "white")
    html_output = html_cell.as_html()
    assert html_output == '<td style="background-color:white">Plain Text</td>'

    # Test cell with no cellformat attribute
    no_format_cell = Cell(value="No Format", x=0, y=0, cellformat=None)
    html_cell = HtmlCell(no_format_cell, "white")
    html_output = html_cell.as_html()
    assert html_output == '<td style="background-color:white">No Format</td>'

    # Test backward compatibility with string values
    html_cell = HtmlCell("Plain String", "white")
    html_output = html_cell.as_html()
    assert html_output == '<td style="background-color:white">Plain String</td>'
