import csv
from pathlib import Path
from typing import Dict, List, Union

import tabulate
from IPython.core.display import display

from datachef.column.base import BaseColumn
from datachef.lookup.engines.horizontal_condition import HorizontalCondition
from datachef.notebook.ipython import in_notebook
from datachef.output.base import BaseOutput
from datachef.selection.selectable import Selectable


class TidyData(BaseOutput):
    def __init__(self, observations: Selectable, *columns):
        """
        A class to generate a basic representation of the
        data as tidy data.
        """

        assert (
            len(columns) > 0
        ), "You need to pass at least one column like object to TidyData"

        assert (
            observations.label is not None
        ), """
                You must have labelled your observation selection before passing
                it to the TidyData constructor.

                You can do so with the .label_as() method.
            """

        self.observations = observations
        self.columns: List[BaseColumn] = columns

        # Don't transform until told to, but once we have
        # only do it once.
        self._data = None

    def __get_representation(self):
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
            display(tabulate.tabulate(data_rows, headers=header_row, tablefmt="html"))
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
        ignored.
        """
        if not self._data:
            grid = []

            header_row = [self.observations.label]
            for column in self.columns:
                header_row.append(column.label)
            grid.append(header_row)

            for observation in self.observations:
                line = [observation.value]
                column_value_dict: Dict[str, str] = {}

                # Resolve the standard columns first
                standard_columns = [
                    x
                    for x in self.columns
                    if not isinstance(x.engine, HorizontalCondition)
                ]
                for column in standard_columns:
                    ob_value = column.resolve_column_cell_from_obs_cell(
                        observation
                    ).value
                    line.append(ob_value)
                    column_value_dict[column.label] = ob_value

                # Now we know the standard column values, resolve the
                # horizontal conditions
                condition_columns = [
                    x for x in self.columns if isinstance(x.engine, HorizontalCondition)
                ]
                priorities = set([x.engine.priority for x in condition_columns])
                for i in priorities:
                    for column in condition_columns:
                        if column.engine.priority == i:
                            ob_value = column.resolve_column_cell_from_obs_cell(
                                observation, column_value_dict
                            )
                            line.append(ob_value)
                            column_value_dict[column.label] = ob_value
                grid.append(line)

            self._data = grid

    def to_csv(
        self,
        path: Union[str, Path],
        write_headers=True,
        write_mode="w",
        *args,
        **kwargs,
    ) -> Path:
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

        with open(path, write_mode) as csvfile:
            tidywriter = csv.writer(csvfile, *args, **kwargs)
            for i, row in enumerate(self._data):
                if i == 0 and not write_headers:
                    continue
                tidywriter.writerow(row)

        return path
