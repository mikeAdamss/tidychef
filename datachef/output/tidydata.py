from __future__ import annotations

import csv
from pathlib import Path
from typing import Callable, Dict, List, Optional, Union

import tabulate
from IPython.core.display import display

from datachef.column.base import BaseColumn
from datachef.exceptions import DroppingNonColumnError, MisalignedHeadersError
from datachef.lookup.engines.horizontal_condition import HorizontalCondition
from datachef.notebook.ipython import in_notebook
from datachef.output.base import BaseOutput
from datachef.selection.selectable import Selectable
from datachef.utils.decorators import dontmutate


class TidyData(BaseOutput):
    def __init__(
        self,
        observations: Selectable,
        *columns,
        obs_apply: Callable = None,
        drop: Optional[List[str]] = None,
    ):
        """
        A class to generate a basic representation of the
        data as tidy data.

        :param observations: The cell selection representing observations.
        :param *columns: 1-n Columns to resolve against the observations.
        :param obs_apply: Callable to make changes to values in the observation column.
        :param drop: Columns by label to drop after cells have been resolved.
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
        self.drop = drop if drop else []
        self.obs_apply = obs_apply

        # Don't transform until told to, but once we have
        # only do it once.
        self._data = None

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
            display(tabulate.tabulate(data_rows, headers=header_row, tablefmt="html"))
            return ""

        # Else return something that'll make sense in a terminal
        return tabulate.tabulate(data_rows, headers=header_row)

    def __repr__(self):  # pragma: no cover
        return self.__get_representation()

    def __str__(self):  # pragma: no cover
        return self.__get_representation()

    def __len__(self):
        self._transform()
        return len(self._data)

    def to_dict(self):
        """
        Outputs the TidyData as a pandas style dictionary, i.e

        {
            column1: [column1value1, column1value2, column1value3],
            column2: [column2value1, column2value2, column2value3],
            etc
        }
        """
        self._transform()
        output_dict = {}

        count = 0
        translater = {}

        for column_name in self._data[0]:
            output_dict[column_name] = []
            translater[count] = column_name
            count += 1

        for row in self._data[1:]:
            for i, item in enumerate(row):
                output_dict[translater[i]].append(item)

        return output_dict

    @staticmethod
    def from_tidy(*tidy_data_objects: TidyData) -> TidyData:
        """
        Creates a class:TidyData object from multiple class:TidyData objects
        provided in the form:

        TidyData.from_tidy(tidydata1, tidydata2, tidydata3)
        """
        return TidyData.from_tidy_list(list(tidy_data_objects))

    @staticmethod
    def from_tidy_list(tidy_data_objects: List[TidyData]) -> TidyData:
        """
        Creates a class:TidyData object from a list of class:TidyData objects
        provided in the form:

        TidyData.from_tidy_list([tidydata1, tidydata2, tidydata3])
        """

        for tidy_data_object in tidy_data_objects:
            assert isinstance(
                tidy_data_object, TidyData
            ), """
            Only objects of type TidyData can be passed into
            TidyData.from_many().
            """

        assert (
            len(tidy_data_objects) > 1
        ), """
            You need to pass 2 or more objects of class TidyData
            into TidyData.from_many()
        """

        tidy_data = tidy_data_objects[0]
        for remaining_tidy_data in tidy_data_objects[1:]:
            tidy_data += remaining_tidy_data

        return tidy_data

    @dontmutate
    def __add__(self, other_tidy_data: TidyData):
        # Make sure all transforms have happened
        self._transform()
        other_tidy_data._transform()

        # Error if we're joining two TidyData objects
        # with different headers
        if self._data[0] != other_tidy_data._data[0]:
            raise MisalignedHeadersError(
                f"""
                You are attempting to sum two tidy data
                outputs but they do not have the same
                column headers.

                TidyData1 headers:
                {self._data[0]}

                TidyData2 headers:
                {other_tidy_data._data[0]}
            """
            )

        # Since the headers match, join all but the header
        # row from the new source
        self._data += other_tidy_data._data[1:]
        return self

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
            drop_count = 0

            header_row = [self.observations.label]
            for column in self.columns:
                if column.label not in self.drop:
                    header_row.append(column.label)
                else:
                    drop_count += 1
            grid.append(header_row)

            # If user has opted to drop a column that does
            # not exist, we need to tell them.
            if drop_count != len(self.drop):
                raise DroppingNonColumnError(
                    f"""
                    You're attempting to drop one or more columns that
                    do not exist in the data.

                    You're dropping: {self.drop}

                    Columns are: {[x.label for x in self.columns]} 
                    """
                )

            for observation in self.observations:
                line = [
                    observation.value
                    if not self.obs_apply
                    else self.obs_apply(observation.value)
                ]
                column_value_dict: Dict[str, str] = {}

                # Resolve the standard columns first
                standard_columns = [
                    x
                    for x in self.columns
                    if not isinstance(x.engine, HorizontalCondition)
                    and x.label not in self.drop
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

                            if column.label not in self.drop:
                                line.append(ob_value)
                            column_value_dict[column.label] = ob_value
                grid.append(line)

            self._data = grid

    def to_csv(
        self,
        path: Union[str, Path],
        write_headers=True,
        write_mode="w",
        **kwargs,
    ):
        """
        Output the TidyData to a csv file.

        This method wraps the standard csv python library,
        the **kwargs provided here are passed
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
            tidywriter = csv.writer(csvfile, **kwargs)
            for i, row in enumerate(self._data):
                if i == 0 and not write_headers:
                    continue
                tidywriter.writerow(row)
