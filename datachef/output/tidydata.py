import csv
from pathlib import Path
from typing import List, Union

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
        self._data = None

    # Note: representations are confirmed via scenarios
    # as contextually changing formatting is a difficult
    # thing to check with unit tests.
    def __get_representation(self):  # pragma: no cover
        """
        Representation logic shared by __str__ and __repr__
        """
        if not self._data:
            self._transform()

        header_row = self._data[0]
        data_rows = self._data[1:]

        # If we're in a notebook, create a nice html display
        if in_notebook():
            header_row = self._data[0]
            data_rows = self._data[1:]
            display(
                HTML(tabulate.tabulate(data_rows, headers=header_row, tablefmt="html"))
            )
            return ""

        # Else return something that'll make sense in a terminal
        return tabulate.tabulate(data_rows, headers=header_row)

    def __repr__(self):  # pragma: no cover
        return self.__get_representation()

    def __str__(self):  # pragma: no cover
        return self.__get_representation()

    def _transform(self):
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
        representation can be accessed via "._data".

        This result is cached so future calls to transform
        will not repopulate this attribute and will be
        ignored - this is so we can freely call things like
        preview functionality ahead of time without repeating
        a potentially resource intensive process.
        """
        if not self._data:
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

            self._data = grid

    def to_csv(self, path: Union[str, Path], *args, **kwargs) -> Path:
        """
        Output the TidyData to a csv file.

        This method wraps the standard csv python library,
        the *args and **kwargs provided here are passed
        through to the csv.csvwriter() constructor.
        https://docs.python.org/3/library/csv.html

        Returns a Path object representing the file that
        has been written to, principally for testing.
        """
        if not self._data:
            self._transform()

        if not isinstance(path, (Path, str)):
            raise ValueError(
                "To output to a file you must provide a pathlib.Path object or a str"
            )

        if isinstance(path, str):
            path = Path(path)

        if not path.parent.exists():
            raise FileNotFoundError(
                f'The specified output directory "{path.parent.absolute()}" for the file "{path.name}" does not exist.'
            )

        with open(path, "w") as csvfile:
            tidywriter = csv.writer(csvfile, *args, **kwargs)
            for row in self._data:
                tidywriter.writerow(row)

        return path
