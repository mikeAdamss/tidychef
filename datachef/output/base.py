from abc import ABCMeta, abstractmethod
from typing import Any, List, Optional

from datachef.selection.selectable import Selectable
from datachef.column.base import BaseColumn

class BaseOutput(metaclass=ABCMeta):
    """
    A class to hold tidy data representations of a data source.

    Note: The purpose of this class is to:
    - 1.) hold the observation data
    - 2.) hold the desired column data
    - 3.) Be able to resolve the correct value of 2 relative to
          any given value of 1

    Do not presume output format. that will vary from use
    case to use case and should remain decoupled.
    """

    def __init__(self,
                 observations: Selectable,
                 columns: List[BaseColumn],
                 *args,
                 **kwargs
                 ):
        """
        A class to hold tidy data representations of a data source.
        """
        self._post_init(observations, columns, *args, **kwargs)
        
    @abstractmethod
    def _post_init(self,
                 observations: Selectable,
                 columns: List[BaseColumn],
                 *args,
                 **kwargs
                 ):
        """
        This is where we hook into whatever the custom behaviour
        of the child class is.
        """

    @abstractmethod
    def __str__(self):
        """
        What happens when someone prints this output.
        """
