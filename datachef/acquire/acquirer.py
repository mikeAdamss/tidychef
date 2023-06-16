"""
Acquire is the principle gateway for acquiring new source data
making http gets where necessary before passing the source into the readers.
"""
from pathlib import Path
from typing import Any, Optional, Callable

from datachef.acquire.base import BaseReader
from datachef.selection.selectable import Selectable
from datachef.utils import fileutils

from dataclasses import dataclass

def acquirer(
        source: Any,
        reader: Optional[BaseReader] = None,
        selectable: Optional[Selectable] = None,
        pre_hook: Optional[Callable] = None,
        post_hook: Optional[Callable] = None,
        **kwargs) -> Selectable:
        """
        """

        # Execute pre load hook
        if pre_hook:
            source = pre_hook(source)

        parsed = reader.parse(
            source,
            selectable=selectable,
            **kwargs)
        
        # Execute post load hook
        if post_hook:
            parsed = post_hook(parsed)
        
        return parsed
