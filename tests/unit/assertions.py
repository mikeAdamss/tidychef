from pivoter.models.source.input import BaseInput


def livetable_tables_have_same_length(input: BaseInput):
    """
    Assert that the Livetable class attributes:

    pristine: class:Table
    filtered: class:Table

    Have matching lengths (number of cells).

    Please note, this should only guaranteed True at the
    point of ingestion before any filtering has taken place.
    """

    # length of filtered table
    flen = len(input.selected_table.filtered.cells)

    # length of pristinr table
    plen = len(input.selected_table.pristine.cells)

    assert flen == plen, (
        f"Length of pristine and filtered table for table {input.selected_table.name}"
        f" do not match. Pristine has {plen} cells, "
        f"Filtered has {flen}"
    )


def pristine_table_has_length(input: BaseInput, expected_len: int):
    """
    Assert that the Livetable class attribute:

    pristine: class:Table

    Has a length (number of cells) matching the expected length.
    """

    pristine_cell_count = len(input.selected_table.pristine.cells)
    assert (
        pristine_cell_count == expected_len
    ), f"For table {input.selected_table.name}, expected {expected_len} cells, got {pristine_cell_count}"
