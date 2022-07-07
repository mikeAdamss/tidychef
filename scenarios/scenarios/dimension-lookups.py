#!/usr/bin/env python
# coding: utf-8
# %%

from pathlib import Path

from datachef import acquire, preview, label, up, down, left, right, filters
from datachef import filters
from datachef.models.dsd.components.dimension import Dimension
from datachef.lookup.engines.direct import Directly

tab = acquire(Path("data/bands.csv"))

obs = tab.filter(filters.is_numeric)
names = tab.excel_ref('B4').expand(right).expand(down).filter(filters.is_not_numeric).is_not_blank()
possessions = tab.excel_ref('C2').expand(right).is_not_blank()
band = tab.excel_ref('A3').expand(right).is_not_blank()

preview(label(obs, "observations"), label(names, "names"), label(possessions, 'possessions'), label(band, 'band'))


# %%


name_dim = Dimension("Names Dim", names, Directly, left)
possession_dim = Dimension("Possession Dim", possessions, Directly, up)

for ob in obs.cells:
    print(f'Ob {ob.value} in {ob._excel_ref()} has:')
    print(f'Name: {name_dim.component.resolve(ob)}')
    print(f'Possession: {possession_dim.component.resolve(ob)}')
    print()


# %%

