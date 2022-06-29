from pathlib import Path
from typing import Optional

from datachef.exceptions import UnalignedTableOperation
from datachef.selection.selectable import Selectable

from .base import BasePreview
from .previewers.html import HtmlPreview


def preview(
    *selections,
    previewer: BasePreview = HtmlPreview,
    path: Path = False,
    end: Optional[str] = None,
    start: Optional[str] = None
):
    """
    Create a preview from one of more selections of cells.
    """

    for s in selections:
        assert isinstance(
            s, Selectable
        ), f"Only selections and keyword arguments can be passed to preview, got {type(s)}"
    selections = list(selections)

    if len(set([s.signature for s in selections])) > 1:
        raise UnalignedTableOperation()

    previewer().print(selections, end=end, start=start, path=path)


def label(selection: Selectable, label: str) -> Selectable:
    """
    Attach a user defined label to a selection for the purposes of
    creating previews.
    """
    selection._label: str = label
    return selection
