from datachef.cardinal.directions import up, down, left, right
from datachef.lookup.engines.direct import Direct
from dataclasses import dataclass
import pytest

from datachef.selection import filters

from os import linesep
from datachef.models.source.cell import Cell
from datachef.selection.selectable import Selectable
from tests.fixtures import fixture_vertical_dimensions, fixture_wide_band_tab
from datachef.selection import datafuncs as dfc


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
        selectable_wide_band_tab.excel_ref('B4').expand(down).is_not_blank() |
        selectable_wide_band_tab.excel_ref('H4').expand(down).is_not_blank()
    )
    assert len(dim.cells) == 8, 'Unexpected selection, have we changed the sample data?'

    direct_left_engine = Direct(dim, left, name="Down Test")

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
        Case("K5", "H5")
    ]:
        ob_cell: Cell = selectable_wide_band_tab.excel_ref(case.obs_ref).cells[0]
        looked_up_cell: Cell = direct_left_engine.resolve(ob_cell)
        looked_up_cell_ref: str = dfc.basecell_to_excel_ref(looked_up_cell)
        assert looked_up_cell_ref == case.expected_cell_ref, (
            f'Expected lookup to resolve to {case.expected_cell_ref}, got {looked_up_cell_ref}'
            f' from options of: {linesep}{direct_left_engine._lookups[looked_up_cell.y]}'
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
        selectable_wide_band_tab.excel_ref('C4').expand(down).is_not_blank() |
        selectable_wide_band_tab.excel_ref('I4').expand(down).is_not_blank()
    )
    assert len(dim.cells) == 8, 'Unexpected selection, have we changed the sample data?'

    direct_left_engine = Direct(dim, right, name="Right Test")

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
        looked_up_cell: Cell = direct_left_engine.resolve(ob_cell)
        looked_up_cell_ref: str = dfc.basecell_to_excel_ref(looked_up_cell)
        assert looked_up_cell_ref == case.expected_cell_ref, (
            f'Expected lookup from {case.obs_ref} direction "{direct_left_engine.direction._direction}"'
            f' to resolve to {case.expected_cell_ref}, got {looked_up_cell_ref}'
            f' from options of: {linesep}{direct_left_engine._lookups[looked_up_cell.y]}'
        )


def test_direct_up_multiple_options_lookup(selectable_vertical_dimensions: Selectable):
    """
    Test that the direct lookup engine resolve visual relationships
    in the required fashion where multiple direct options are
    availible.
    """
    
    dim = selectable_vertical_dimensions.excel_ref('A4').expand(down).expand(right) \
        .filter(filters.is_not_numeric).is_not_blank()

    assert len(dim.cells) == 12, 'Unexpected selection, have we changed the sample data?'

    direct_left_engine = Direct(dim, up, name="Up Test")

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
        looked_up_cell: Cell = direct_left_engine.resolve(ob_cell)
        looked_up_cell_ref: str = dfc.basecell_to_excel_ref(looked_up_cell)
        assert looked_up_cell_ref == case.expected_cell_ref, (
            f'Expected lookup from {case.obs_ref} direction "{direct_left_engine.direction._direction}"'
            f' to resolve to {case.expected_cell_ref}, got {looked_up_cell_ref}'
            f' from options of: {linesep}{direct_left_engine._lookups[looked_up_cell.y]}'
        )


def test_direct_down_multiple_options_lookup(selectable_vertical_dimensions: Selectable):
    """
    Test that the direct lookup engine resolve visual relationships
    in the required fashion where multiple direct options are
    availible.
    """
    
    dim = selectable_vertical_dimensions.excel_ref('A4').expand(down).expand(right) \
        .filter(filters.is_not_numeric).is_not_blank()

    assert len(dim.cells) == 12, 'Unexpected selection, have we changed the sample data?'

    direct_left_engine = Direct(dim, down, name="Down Test")

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
        looked_up_cell: Cell = direct_left_engine.resolve(ob_cell)
        looked_up_cell_ref: str = dfc.basecell_to_excel_ref(looked_up_cell)
        assert looked_up_cell_ref == case.expected_cell_ref, (
            f'Expected lookup from {case.obs_ref} direction "{direct_left_engine.direction._direction}"'
            f' to resolve to {case.expected_cell_ref}, got {looked_up_cell_ref}'
            f' from options of: {linesep}{direct_left_engine._lookups[looked_up_cell.y]}'
        )
