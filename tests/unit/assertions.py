from pivoter.models.source import Input, LiveTable


def livetable_tables_have_same_length(input: Input):
    """
    Assert that the Livetable class attributes:

    pristine: class:Table
    filtered: class:Table

    Have matching lengths (number of cells).

    Please note, this should only guaranteed True at the
    point of ingestion before any filtering has taken place.
    """

    assert input.selected_table._table_lengths_match(), (
        f"Length of pristine and filtered table for table {input.selected_table.name}"
        f" do not match. Pristine has {len(input.selected_table.pristine.cells)} cells, "
        f"Filtered has {len(input.selected_table.filtered.cells)}"
    )


def pristine_table_has_length(input: Input, expected_len: int):
    """
    Assert that the Livetable class attribute:

    pristine: class:Table

    Has a length (number of cells) matching the expected length.
    """
    assert input.selected_table.pristine._has_length(
        expected_len
    ), f"For table {input.selected_table.name}, expected {expected_len} cells, got {len(input.selected_table.pristine.cells)}"
