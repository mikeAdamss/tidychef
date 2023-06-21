from pathlib import Path
from typing import Dict, Union

from IPython.display import HTML, display

from datachef.exceptions import OutputPassedToPreview, UnalignedTableOperation
from datachef.output.base import BaseOutput
from datachef.selection.selectable import Selectable

from ...ipython import in_notebook
from .table import get_preview_table_as_html


def preview(
    *selections,
    path: Path = None,
    bounded: Union[str, Dict[str, str]] = None,
    border_cells: str = "lightgrey",
    blank_cells: str = "white",
    warning_colour: str = "#ff8080",
    with_excel_notations=True,
    multiple_selection_warning: bool = True,
):
    """
    Create a preview from one of more selections of cells.
    """
    if isinstance(selections[0], BaseOutput):
        raise OutputPassedToPreview(
            """
            You cannot call preview an output.
            
            A preview displays the source data and the visual relationships you've
            you've declared within it. Once you have created an output (for example 
            created a TidyData() class) you can no longer preview it using this
            function.

            If you want to preview an output you can just print() it.
            """
        )

    for s in selections:
        assert isinstance(
            s, Selectable
        ), f"Only selections and keyword arguments can be passed to preview, got {type(s)}"
    selections = list(selections)

    if len(set([s.signature for s in selections])) > 1:
        raise UnalignedTableOperation()

    html_as_str = get_preview_table_as_html(
        selections,
        bounded=bounded,
        multiple_selection_warning=multiple_selection_warning,
        with_excel_notations=with_excel_notations,
        border_cells=border_cells,
        warning_colour=warning_colour,
        blank_cells=blank_cells,
    )

    if path:
        with open(path, "w") as f:
            f.write(html_as_str)
    else:
        display(HTML(html_as_str))
