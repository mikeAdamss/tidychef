import pytest

from datachef.cardinal.directions import above
from datachef.lookup.engines.direct import Directly
from datachef.models.dsd.components.dimension import (
    ComponentDimensionConstant,
    ComponentDimensionDirect,
    Dimension,
)
from datachef.models.source.cell import Cell, VirtualCell
from datachef.selection import datafuncs as dfc
from datachef.selection.selectable import Selectable
from tests.fixtures import fixture_simple_one_tab


@pytest.fixture
def selectable_simple1():
    return fixture_simple_one_tab()


def test_dimension_constant_constructor():
    """
    Test that where minimum params are supplied a dimension
    of type DimensionConstant is created
    """

    dimension = Dimension("A constant dimension", constant="foo")
    assert isinstance(dimension.component, ComponentDimensionConstant), (
        f"Expecting dimension type {ComponentDimensionConstant}"
        f", for {dimension.component}"
    )

    vcell: VirtualCell = dimension.component.resolve("doesnt matter")
    assert isinstance(vcell, VirtualCell)

    expected = "foo"
    resolved = vcell.value
    assert resolved == expected, f'Expecting: "{expected}", got: {resolved}'


def test_dimension_direct_constructor(selectable_simple1: Selectable):
    """
    Test that where appropriate params are supplied a dimension
    of type DimensionConstant is created
    """

    dim_selection = selectable_simple1.excel_ref("A1")
    dimension = Dimension(
        "A dimension with a vertical relationship", dim_selection, Directly, above
    )
    assert isinstance(dimension.component, ComponentDimensionDirect), (
        f"Expecting dimension type {ComponentDimensionDirect}"
        f", for {dimension.component}"
    )

    resolved: Cell = dimension.component.resolve(
        selectable_simple1.excel_ref("A2").cells[0]
    )
    assert isinstance(resolved, Cell)
    assert dfc.basecell_to_excel_ref(resolved) == "A1"


def test_failed_construction_repr():
    """
    Test that where an issue is encoutered constructing the component
    we get the expected feedback.
    """

    with pytest.raises(Dimension.contextual_exception) as err_info:
        Dimension("Nothing uses only one arg")
