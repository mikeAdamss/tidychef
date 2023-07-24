from tidychef.notebook.preview.html.tidy_data import tidy_data_as_html_table_string
from tests.fixtures.helpers import path_to_fixture


def test_tidy_data_as_html_table_string():
    """
    Test that our conversation of tidydata lists of lists
    works as intended.
    """

    html_str: str = tidy_data_as_html_table_string(
        [
            ["Header1", "Header2"],
            ["Row1Value1", "Row1Value2"],
            ["Row2Value1", "Row2Value2"],
        ]
    )

    with open(path_to_fixture("preview", "table-print.html")) as f:
        expected_html_str = f.read()

    assert html_str == expected_html_str
