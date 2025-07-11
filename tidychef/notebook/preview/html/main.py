from pathlib import Path
from typing import Union

from IPython.display import HTML, display

from tidychef.exceptions import OutputPassedToPreview, UnalignedTableOperation
from tidychef.models.source.table import LiveTable
from tidychef.output.base import BaseOutput

from .table import get_preview_table_as_html


def preview(
    *selections,
    path: Union[Path, str] = None,
    bounded: str = None,
    border_cells: str = "lightgrey",
    blank_cells: str = "white",
    warning_colour: str = "#ff8080",
    show_excel: bool = True,
    show_xy: bool = False,
    multiple_selection_warning: bool = True,
    selection_boundary: bool = False,
    label: str = None,
):
    """
    Create a preview from one of more selections of cells.

    :param *selections: 1-n tidychef selectables of inheritors of
    that will inform the preview.
    :param path: A Path or string representation of for where
    we want to write a html preview to local.
    :bounded param:
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
            s, LiveTable
        ), f"Only selections and keyword arguments can be passed to preview, got {type(s)}"
    selections = list(selections)

    if len(set([s.signature for s in selections])) > 1:
        raise UnalignedTableOperation(
            "Selections can only be combined or previewed in combination "
            "if they are taken from the exact same table as taken from a single "
            "instance of a parsed input."
        )

    html_as_str = get_preview_table_as_html(
        selections,
        bounded=bounded,
        multiple_selection_warning=multiple_selection_warning,
        show_excel=show_excel,
        show_xy=show_xy,
        border_cells=border_cells,
        warning_colour=warning_colour,
        blank_cells=blank_cells,
        selection_boundary=selection_boundary,
    )

    if path:
        # If writing to an explain path, we write append
        write_mode = "a" if selection_boundary else "w"
        with open(path, write_mode) as f:
            f.write(html_as_str)
    else:
        display(HTML(html_as_str))
