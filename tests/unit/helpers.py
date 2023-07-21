import os
from pathlib import Path
from typing import List

from datachef import datafuncs as dfc
from datachef.models.source.cell import BaseCell


def qcel(excel_ref) -> BaseCell:
    """
    "QueryCell" - test helper to create a single BaseCell object from
    an appropriate excel reference.
    """
    assert ":" not in excel_ref
    cell: BaseCell = dfc.single_excel_ref_to_basecell(excel_ref)
    return cell


def qcels(excel_ref) -> List[BaseCell]:
    """
    "QueryCells" - test helper to create a list of 2 or more BaseCell objects from
    an appropriate excel reference.
    """
    assert ":" in excel_ref
    cells: List[BaseCell] = dfc.multi_excel_ref_to_basecells(excel_ref)
    return cells


def assert_csvs_match(path_to_newly_created_csv: Path, path_to_csv_thats_correct: Path):
    """
    Given a path to two csvs, read them and do
    a line by line comparison to confirm that the
    first matches the second.
    """

    with open(path_to_newly_created_csv) as csv_data_got:
        output_rows_got = csv_data_got.readlines()

    with open(path_to_csv_thats_correct) as csv_data_expected:
        output_rows_expected = csv_data_expected.readlines()

    assert len(output_rows_got) == len(
        output_rows_expected
    ), "Csv output and expected csv output have a different number of rows"

    for i in range(0, len(output_rows_got)):
        row_got = output_rows_got[i]
        row_expected = output_rows_expected[i]

        assert (
            row_got == row_expected
        ), f"""
                Csv output does not match fixtures.

                Newly created row number {i} of:
                {row_got}
                Does not match the expected row {i} of:
                {row_expected}

                --------
                new output path: {path_to_newly_created_csv.resolve()} 
                fixture_path: {path_to_csv_thats_correct.resolve()}
                """

    os.remove(path_to_newly_created_csv.resolve())
