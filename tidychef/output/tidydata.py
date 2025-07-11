from __future__ import annotations

import csv
from pathlib import Path
from typing import Callable, Dict, List, Optional, Union, Tuple

import tabulate
from IPython.display import HTML, display

from tidychef.column.base import BaseColumn
from tidychef.exceptions import DroppingNonColumnError, MisalignedHeadersError
from tidychef.lookup.engines.horizontal_condition import HorizontalCondition
from tidychef.models.source.cell import VirtualCell
from tidychef.models.source.table import LiveTable
from tidychef.notebook.ipython import in_notebook
from tidychef.notebook.preview.html.tidy_data import tidy_data_as_html_table_string
from tidychef.output.base import BaseOutput
from tidychef.utils.decorators import dontmutate


class TidyData(BaseOutput):
    def __init__(
        self,
        observations: LiveTable,
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
        self.columns: Tuple[BaseColumn] = columns
        self.drop = drop if drop else []
        self.obs_apply = obs_apply

        # Don't transform until told to, but once we have
        # only do it once.
        self._data = None


    def add_column(self, column: BaseColumn):
        """
        Add a column to the TidyData object.

        This method can only be called before the first
        transformation has been run, i.e. before the first
        call to ._transform().
        
        :param column: A BaseColumn object to add to the TidyData.
        """

        assert self._data is None, """
        You can only add columns to TidyData before the first
        transformation has been run. If you want to add a column
        after the first transformation, you need to create a new
        TidyData object with the new column included.
        """

        assert isinstance(
            column, BaseColumn
        ), "You can only add columns of type BaseColumn to TidyData"

        self.columns += (column,)


    def __get_representation(self):  # pragma: no cover
        """
        Representation logic shared by __str__ and __repr__
        """
        if not self._data:
            self._transform()

        table_as_strings = self._data_as_table_of_strings()
        header_row = table_as_strings[0]
        data_rows = table_as_strings[1:]

        # If we're in a notebook, create a nice html display
        if in_notebook():
            display(HTML(tidy_data_as_html_table_string(table_as_strings)))
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

    def _data_as_table_of_strings(self) -> List[List[str]]:
        """
        Generates a table of strings from a table of Cells.

        So turns something like this:

        [
         [ Cell(x=1, y=2, value="Ray"), Cell(x=41, y=2, value="Egon") ],
         [ Cell(x=9, y=5, value="Peter"), Cell(x=0, y=12, value="Winston") ]
        ]

        Into something like this:

        [
         [ "Ray", "Egon" ],
         [ "Peter", "Winston" ]
        ]
        """
        string_table = []
        self._transform()
        for row in self._data:
            string_row = [x.value for x in row]
            string_table.append(string_row)
        return string_table

    def to_dict(self) -> dict:
        """
        Outputs the TidyData as a pandas style dictionary, i.e

        {
            column1: [column1value1, column1value2, column1value3],
            column2: [column2value1, column2value2, column2value3],
            etc
        }
        """
        self._transform()
        output_dict: Dict[str, List[str]] = {}

        count = 0
        translater: Dict[i, str] = {}

        for column_header_cell in self._data[0]:
            output_dict[column_header_cell.value] = []
            translater[count] = column_header_cell.value
            count += 1

        for row in self._data[1:]:
            for i, item in enumerate(row):
                output_dict[translater[i]].append(item.value)

        return output_dict

    @staticmethod
    def from_tidy(*tidy_data_objects: TidyData) -> TidyData:
        """
        Creates a class:TidyData object from multiple class:TidyData objects
        provided in the form:

        TidyData.from_tidy(tidydata1, tidydata2, tidydata3)

        :param *tidy_data_objects: 1-n populated tidy data objects that we
        want to join together.
        """
        return TidyData.from_tidy_list(list(tidy_data_objects))

    @staticmethod
    def from_tidy_list(tidy_data_objects: List[TidyData]) -> TidyData:
        """
        Creates a class:TidyData object from a list of class:TidyData objects
        provided in the form:

        TidyData.from_tidy_list([tidydata1, tidydata2, tidydata3])

        :param tidy_data_objects: A list of 1-n populated tidy data objects
        that we want to join together.
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
            into to join multiple TidyData sources into one.
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

        # Dev note:
        # The key point here is we're assembling a table
        # of Cell and VirtualCell objects, not a table
        # of the strings that each represent.
        # This is so we maintain provenance information
        # regarding how and from where each value was
        # acquired.

        if not self._data:
            grid = []
            drop_count = 0

            # Observations always has the table name so
            # spread it around to cover those columns that
            # are created via static methods.
            for column in self.columns:
                column._table == self.observations._name

            # We need to carefully construct our lists of lists
            # such that the HorizontalCondition columns are created last
            # Ordering will be restored at the end via this list.
            ordered_column_header_cells = [
                VirtualCell(value=self.observations.label)
            ] + [VirtualCell(value=x.label) for x in self.columns]

            # Obs label
            if self.observations.label in self.drop:
                unordered_header_row_cells = []
                drop_count += 1
            else:
                unordered_header_row_cells = [
                    VirtualCell(value=self.observations.label)
                ]

            # Standard Column labels
            for column in [
                x for x in self.columns if not isinstance(x.engine, HorizontalCondition)
            ]:
                if column.label not in self.drop:
                    unordered_header_row_cells.append(VirtualCell(value=column.label))
                else:
                    drop_count += 1

            # Horizontal Condition
            for column in [
                x for x in self.columns if isinstance(x.engine, HorizontalCondition)
            ]:
                if column.label not in self.drop:
                    unordered_header_row_cells.append(VirtualCell(value=column.label))
                else:
                    drop_count += 1

            # Conditional column labels
            header_row = []
            for column_header_cell in ordered_column_header_cells:
                if column_header_cell in unordered_header_row_cells:
                    header_row.append(column_header_cell)

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
                row_as_dict = {}

                # note we ALWAYS want values in the column_value_dict
                # regardless of whether we're dropping the column
                column_value_dict: Dict[str, str] = {}
                column_value_dict[self.observations.label] = observation.value

                if self.observations.label not in self.drop:
                    if self.obs_apply is not None:
                        observation.value = self.obs_apply(observation.value)
                    row_as_dict[self.observations.label] = observation

                # Resolve the standard columns first
                standard_columns = [
                    x
                    for x in self.columns
                    if not isinstance(x.engine, HorizontalCondition)
                ]
                for column in standard_columns:
                    column_cell = column.resolve_column_cell_from_obs_cell(observation)
                    column_value_dict[column.label] = column_cell.value
                    if column.label not in self.drop:
                        row_as_dict[column.label] = column_cell

                # Now we know the standard column values, resolve the
                # horizontal conditions
                condition_columns = [
                    x for x in self.columns if isinstance(x.engine, HorizontalCondition)
                ]
                priorities = set([x.engine.priority for x in condition_columns])
                for i in priorities:
                    for column in condition_columns:
                        if column.engine.priority == i:
                            column_cell = column.resolve_column_cell_from_obs_cell(
                                observation, column_value_dict
                            )

                            column_value_dict[column.label] = column_cell.value
                            if column.label not in self.drop:
                                row_as_dict[column.label] = column_cell

                # Order for output
                line = []
                for column_cell in ordered_column_header_cells:
                    cell_wanted = row_as_dict.get(column_cell.value, None)
                    if cell_wanted is not None:
                        line.append(cell_wanted)

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

        :param path: The location we want to output the
        csv to.
        :param write_headers: Whether or not to include the
        headers when writing to csv.
        :param write_mode: The mode with which to open
        the python file object. Defaults to "w".
        """
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
            for i, row in enumerate(self._data_as_table_of_strings()):
                if i == 0 and not write_headers:
                    continue
                tidywriter.writerow(row)

    def drop_duplicates(
        self,
        print_duplicates: bool = False,
        csv_duplicate_path: Union[str, Path] = None,
    ):
        """
        Drop duplicates from our tidydata.

        :param print_duplicates: Do we want a human friendly report showing
        each duplicate row that has been dropped.
        :param csv_duplicate_path: Path to output a csv containing each duplicate
        row.
        """
        self._transform()
        unique = []

        non_unique = []
        lines = [
            "Removed duplicate instances of the following row(s):",
            "-----------------------------------------------------",
        ]

        for row in self._data:
            if row not in unique:
                unique.append(row)
            else:
                if print_duplicates:  # pragma: no cover
                    lines.append(",".join([x.value for x in row]))
                if csv_duplicate_path:
                    non_unique.append([x.value for x in row])

        if print_duplicates:  # pragma: no cover
            for line in lines:
                print(line)

        if csv_duplicate_path:
            if not isinstance(csv_duplicate_path, Path):
                csv_duplicate_path = Path(csv_duplicate_path)

            with open(csv_duplicate_path, "w") as csvfile:
                duplicates_writer = csv.writer(csvfile)
                for row in non_unique:
                    duplicates_writer.writerow(row)

        self._data = unique
        return self
