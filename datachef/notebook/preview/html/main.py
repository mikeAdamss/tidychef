from pathlib import Path
from typing import Optional

from datachef.exceptions import OutputPassedToPreview, UnalignedTableOperation
from datachef.output.base import BaseOutput
from datachef.selection.selectable import Selectable

from IPython.display import HTML, display

from ...ipython import in_notebook
from .table import get_preview_table_as_html

def preview(
    *selections,
    path: Path = False,
    end: Optional[str] = None,
    start: Optional[str] = None,
    multiple_selection_warning: bool = True,
    force_preview: bool = False
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
    
    if not path and not in_notebook and not force_preview:
        raise Exception('''
            To preview, you must do one of:

            - (a) Pass a path= keyword to preview to specify the destination of the
                 html preview.
             -(b) Be running the code in a Jupyter/Ipython notebook

             To override this error and attempt a preview anyway pass
             force_preivew=True into the preview() constructor.
        ''')

    for s in selections:
        assert isinstance(
            s, Selectable
        ), f"Only selections and keyword arguments can be passed to preview, got {type(s)}"
    selections = list(selections)

    if len(set([s.signature for s in selections])) > 1:
        raise UnalignedTableOperation()

    
    html_as_str = get_preview_table_as_html(
        selections,
        end=end,
        start=start,
        multiple_selection_warning=multiple_selection_warning,
    )

    if path:
        # Write  to a a place!
        ...
    else:
        if in_notebook:
            display(HTML(html_as_str))
        else:
            print(html_as_str)

