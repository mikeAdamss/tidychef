import copy
from dataclasses import dataclass
from os import linesep

import pytest

from datachef.direction.directions import down, left, right, up
from datachef.column.column import Column
from datachef.exceptions import (
    FailedLookupError,
    MissingDirectLookupError,
    MissingLabelError,
    UnknownDirectionError,
)
from datachef.lookup.engines.direct import Directly
from datachef.models.source.cell import Cell
from datachef.selection import datafuncs as dfc
from datachef.selection import filters
from datachef.selection.selectable import Selectable
from tests.fixtures import fixture_vertical_dimensions, fixture_wide_band_tab


@pytest.fixture
def selectable_wide_band_tab():
    return fixture_wide_band_tab()


@pytest.fixture
def selectable_vertical_dimensions():
    return fixture_vertical_dimensions()


def test_direct_left_multiple_options_lookup(selectable_wide_band_tab: Selectable):
    """
    Test that the direct lookup engine resolve visual relationships
    in the required fashion where multiple direct options are
    availible.
    """

    dim = (
        selectable_wide_band_tab.excel_ref("B4").expand(down).is_not_blank()
        | selectable_wide_band_tab.excel_ref("H4").expand(down).is_not_blank()
    )
    assert len(dim.cells) == 8, "Unexpected selection, have we changed the sample data?"

    direct_left_engine = Directly("", dim, left)

    @dataclass
    class Case:
        obs_ref: str
        expected_cell_ref: str

    for case in [
        Case("C4", "B4"),
        Case("D4", "B4"),
        Case("E4", "B4"),
        Case("C6", "B6"),
        Case("I4", "H4"),
        Case("J4", "H4"),
        Case("K5", "H5"),
    ]:
        ob_cell: Cell = selectable_wide_band_tab.excel_ref(case.obs_ref).cells[0]
        looked_up_cell: Cell = direct_left_engine.resolve(ob_cell)
        looked_up_cell_ref: str = dfc.basecell_to_excel_ref(looked_up_cell)
        assert looked_up_cell_ref == case.expected_cell_ref, (
            f"Expected lookup to resolve to {case.expected_cell_ref}, got {looked_up_cell_ref}"
            f" from options of: {linesep}{direct_left_engine._lookups[looked_up_cell.y]}"
        )


def test_direct_right_multiple_options_lookup(selectable_wide_band_tab: Selectable):
    """
    Test that the direct lookup engine resolve visual relationships
    in the required fashion where multiple direct options are
    availible.
    """

    # To save us a fixture We're just going to reverse the logic and lookup from
    # what would be dimension items to what would be observations
    dim = (
        selectable_wide_band_tab.excel_ref("C4").expand(down).is_not_blank()
        | selectable_wide_band_tab.excel_ref("I4").expand(down).is_not_blank()
    )
    assert len(dim.cells) == 8, "Unexpected selection, have we changed the sample data?"

    direct_right_engine = Directly("", dim, right)

    @dataclass
    class Case:
        obs_ref: str
        expected_cell_ref: str

    for case in [
        Case("B4", "C4"),
        Case("B6", "C6"),
        Case("H4", "I4"),
        Case("H6", "I6"),
    ]:
        ob_cell: Cell = selectable_wide_band_tab.excel_ref(case.obs_ref).cells[0]
        looked_up_cell: Cell = direct_right_engine.resolve(ob_cell)
        looked_up_cell_ref: str = dfc.basecell_to_excel_ref(looked_up_cell)
        assert looked_up_cell_ref == case.expected_cell_ref, (
            f'Expected lookup from {case.obs_ref} direction "{direct_right_engine.direction.name}"'
            f" to resolve to {case.expected_cell_ref}, got {looked_up_cell_ref}"
            f" from options of: {linesep}{direct_right_engine._lookups[looked_up_cell.y]}"
        )


def test_direct_up_multiple_options_lookup(selectable_vertical_dimensions: Selectable):
    """
    Test that the direct lookup engine resolve visual relationships
    in the required fashion where multiple direct options are
    availible.
    """

    dim = (
        selectable_vertical_dimensions.excel_ref("A4")
        .expand(down)
        .expand(right)
        .filter(filters.is_not_numeric)
        .is_not_blank()
    )

    assert (
        len(dim.cells) == 12
    ), "Unexpected selection, have we changed the sample data?"

    direct_up_engine = Directly("", dim, up)

    @dataclass
    class Case:
        obs_ref: str
        expected_cell_ref: str

    for case in [
        Case("B6", "B4"),
        Case("B14", "B12"),
        Case("A18", "A12"),
        Case("D16", "D12"),
    ]:
        ob_cell: Cell = selectable_vertical_dimensions.excel_ref(case.obs_ref).cells[0]
        looked_up_cell: Cell = direct_up_engine.resolve(ob_cell)
        looked_up_cell_ref: str = dfc.basecell_to_excel_ref(looked_up_cell)
        assert looked_up_cell_ref == case.expected_cell_ref, (
            f'Expected lookup from {case.obs_ref} direction "{direct_up_engine.direction.name}"'
            f" to resolve to {case.expected_cell_ref}, got {looked_up_cell_ref}"
            f" from options of: {linesep}{direct_up_engine._lookups[looked_up_cell.y]}"
        )


def test_direct_down_multiple_options_lookup(
    selectable_vertical_dimensions: Selectable,
):
    """
    Test that the direct lookup engine resolve visual relationships
    in the required fashion where multiple direct options are
    availible.
    """

    dim = (
        selectable_vertical_dimensions.excel_ref("A4")
        .expand(down)
        .expand(right)
        .filter(filters.is_not_numeric)
        .is_not_blank()
    )

    assert (
        len(dim.cells) == 12
    ), "Unexpected selection, have we changed the sample data?"

    direct_down_engine = Directly("", dim, down)

    @dataclass
    class Case:
        obs_ref: str
        expected_cell_ref: str

    for case in [
        Case("B6", "B12"),
        Case("A8", "A12"),
        Case("E14", "E20"),
        Case("B17", "B20"),
    ]:
        ob_cell: Cell = selectable_vertical_dimensions.excel_ref(case.obs_ref).cells[0]
        looked_up_cell: Cell = direct_down_engine.resolve(ob_cell)
        looked_up_cell_ref: str = dfc.basecell_to_excel_ref(looked_up_cell)
        assert looked_up_cell_ref == case.expected_cell_ref, (
            f'Expected lookup from {case.obs_ref} direction "{direct_down_engine.direction.name}"'
            f" to resolve to {case.expected_cell_ref}, got {looked_up_cell_ref}"
            f" from options of: {linesep}{direct_down_engine._lookups[looked_up_cell.y]}"
        )


def test_bad_direction_param(selectable_vertical_dimensions: Selectable):
    """
    Test that the appropriate error is raised where an incorrect
    direction parameter is provided.
    """

    with pytest.raises(UnknownDirectionError):
        Directly("", selectable_vertical_dimensions, "not a direction")


def test_no_direction_lookup(selectable_vertical_dimensions: Selectable):
    """
    Test that where a user has specified a direct lookup where one
    does not exist, a suitable error is raised.
    """

    dim = selectable_vertical_dimensions.excel_ref("A1")
    ob: Cell = selectable_vertical_dimensions.excel_ref("B10").cells[0]

    # A1 is not up from B10, so an error should get raised
    with pytest.raises(MissingDirectLookupError):
        direct_up_engine = Directly("", dim, up)
        direct_up_engine.resolve(ob)


def test_malformed_class_err(selectable_vertical_dimensions: Selectable):
    """
    Conform a suitable error is raised if an unexpected or malformed
    direction is passed.
    """

    badup = copy.deepcopy(up)
    badup.name = "sideways"

    dim = selectable_vertical_dimensions.excel_ref("A1")
    ob: Cell = selectable_vertical_dimensions.excel_ref("A10").cells[0]

    # badup should raise an error
    with pytest.raises(UnknownDirectionError):
        direct_up_engine = Directly("", dim, badup)
        direct_up_engine.resolve(ob)


def test_failed_lookup_err(selectable_vertical_dimensions: Selectable):
    """
    Conform a suitable error is raised where we do have cells on the
    coirrect axis, but none in the considered cardinal direction.
    """

    dim = selectable_vertical_dimensions.excel_ref("A10")
    ob: Cell = selectable_vertical_dimensions.excel_ref("A1").cells[0]

    # we have a dimension item in A10 ... but that's not up from A1
    with pytest.raises(FailedLookupError):
        direct_up_engine = Directly("", dim, up)
        direct_up_engine.resolve(ob)


def test_directly_wrapper_via_selectable_down(
    selectable_vertical_dimensions: Selectable,
):
    """
    Test that directly down can be correctly instantiated via the wrapper
    provided by the Selectiable class.
    """

    column_selection = selectable_vertical_dimensions.excel_ref("A1").label_as("foo")
    ob: Cell = selectable_vertical_dimensions.excel_ref("A10").cells[0]
    resolved_cell: Cell = Column(
        column_selection.finds_observations_directly(down)
    ).resolve_column_cell_from_obs_cell(ob)
    assert resolved_cell._excel_ref() == "A1"


def test_directly_raises(selectable_vertical_dimensions: Selectable):
    """
    Test that where we try and instantiate a Directly lookup engine without
    a label the expected error is raised.
    """

    column_selection = selectable_vertical_dimensions.excel_ref("A1")

    with pytest.raises(MissingLabelError):
        Column(column_selection.finds_observations_directly(up))
