"""
.. include:: ./README.md
"""
from .common import (
    all_used_x_indicies,
    all_used_y_indicies,
    assert_quadrilaterals,
    cell_is_not_within,
    cell_is_within,
    cells_not_in,
    cells_on_x_index,
    cells_on_y_index,
    exactly_matched_xy_cells,
    exactly_matching_xy_cell,
    get_outlier_indicies,
    matching_xy_cells,
    maximum_x_offset,
    maximum_y_offset,
    minimum_x_offset,
    minimum_y_offset,
    specific_cell_from_xy,
)
from .excel import (
    any_excel_ref_as_wanted_basecells,
    assert_excel_ref_within_cells,
    basecell_to_excel_ref,
    basecells_to_excel_ref,
    multi_excel_ref_to_basecells,
    single_excel_column_to_x_index,
    single_excel_ref_to_basecell,
    single_excel_row_to_y_index,
)
from .ordering import (
    order_cells_bottomtop_leftright,
    order_cells_bottomtop_rightleft,
    order_cells_leftright_bottomtop,
    order_cells_leftright_topbottom,
    order_cells_rightleft_bottomtop,
    order_cells_rightleft_topbottom,
    order_cells_topbottom_leftright,
    order_cells_topbottom_rightleft,
)
