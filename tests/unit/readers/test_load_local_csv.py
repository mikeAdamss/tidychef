from pathlib import Path
import pytest

from pivoter.models.source.input import BaseInput
from pivoter.readers import reader
from pivotertesthelpers import path_to_fixture
import assertions


def test_read_local_csv_from_path():
    """
    Test local file loader for csv from path
    """
    csv_path: Path = path_to_fixture("csv", "simple.csv")
    input: BaseInput = reader.read_local(csv_path)

    assertions.livetable_tables_have_same_length(input)
    assertions.pristine_table_has_length(input, 12)


def test_read_local_csv_from_str():
    """
    Test local file loader for csv from str
    """
    csv_path: Path = path_to_fixture("csv", "simple.csv")
    input: BaseInput = reader.read_local(str(csv_path.absolute()))

    assertions.livetable_tables_have_same_length(input)
    assertions.pristine_table_has_length(input, 12)
