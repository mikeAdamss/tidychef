from typing import List

import tabulate
from IPython.core.display import HTML, display

from datachef.column.base import BaseColumn
from datachef.output.base import BaseOutput
from datachef.selection.selectable import Selectable
from datachef.utils.notebooks.ipython import in_notebook


class TidyData(BaseOutput):
    def __init__(
        self,
        observations: Selectable,
        columns: List[BaseColumn],
        observation_label: str = "Value",
    ):
        """
        A class to generate a basic representation of the
        data as tidy data.
        """
        self.observations = observations
        self.columns = columns
        self.observation_label = observation_label

        # Don't transform until told to, but once we have
        # only do it once.
        self.data = None

    # Note: representations are confirmed via scenarios
    def __get_representation(self):
        """
        Representation logic shared by __str__ and __repr__
        """
        if not self.data:
            self.transform()

        header_row = self.data[0]
        data_rows = self.data[1:]

        # If we're in a notebook, give a nice
        # html display
        if in_notebook():
            header_row = self.data[0]
            data_rows = self.data[1:]
            display(
                HTML(tabulate.tabulate(data_rows, headers=header_row, tablefmt="html"))
            )
            return ""

        return tabulate.tabulate(data_rows, headers=header_row)

    def __repr__(self):
        return self.__get_representation()

    # Note: string representations are confirmed via scenarios
    def __str__(self):  # pragma: no cover
        return self.__get_representation()

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
                    line.append(
                        column.resolve_column_cell_from_obs_cell(observation).value
                    )
                grid.append(line)

            self.data = grid
