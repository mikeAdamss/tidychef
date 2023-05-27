from typing import List, Optional

import tabulate

from datachef.selection.selectable import Selectable
from datachef.column.base import BaseColumn
from datachef.output.base import BaseOutput

class TidyData(BaseOutput):
    """
    A class to generate a basic representation of the
    data as tidy data.
    
    Example:

    | Value | Sex     | Age  |
    | 1     | Male    | 18   |
    | 2     | Male    | 45   |
    | 3     | Female  | 32   |
    | 4     | Female  | 18   |
    """

    def _post_init(self,
                 observations: Selectable,
                 columns: List[BaseColumn],
                 observation_label: str = "Value",
                 *args,
                 **kwargs
                 ):
        """
        A class to hold tidy data representations of a data source
        """
        # Don't transform until told, but once we do
        # keep hold of it.
        self.transform_cached = None

        self.observations = observations
        self.columns = columns
        self.observation_label = observation_label

    def __str__(self):
        """
        When printed, represent the 
        """
        if not self.transform_cached:
            self.transform()
        tabulate(self.transform_cached)

    def transform(self):
        """
        
        """
        grid = []

        header_row = [self.observation_label]
        for column in self.columns:
            header_row.append(column.label)
        grid.append(header_row)

        for observation in self.observations:
            line = [observation.value]
            for column in self.columns:
                line.append(column.resolve_column_cell_from_obs_cell(observation).value)
            grid.append(line)

        self.transform_cached = grid
