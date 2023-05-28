from typing import List

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

    def __init__(self,
                 observations: Selectable,
                 columns: List[BaseColumn],
                 observation_label: str = "Value"
                 ):
        """
        A class to hold tidy data representations of a data source
        """
        self.observations = observations
        self.columns = columns
        self.observation_label = observation_label

        # Don't transform until told to, but once we have
        # only do it once.
        self.data = None

    def __str__(self):
        """
        When printed, display what the ouput will
        look like in a use friendly way. 
        """
        if not self.data:
            self.transform()
        tabulate(self.data)

    def transform(self):
        """
        Uses the column relationships defined to create an
        internal (to this class) representation of tidy data.

        This representation is in the form of:

        [
            [header1,header2,header3],
            [observation1, column2value1, column3value1]
            ...etc... 
        ]

        Once this method has been ran, this internal
        representation can be access via ".data".

        This result is cached so future calls to transform
        will not repopulate this attribute and will be
        ignored - this is so we can freely call things like
        preview functionality ahead of time without repeating
        a potentially resource intensive process.
        """
        if not self.data:
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

            self.data = grid
