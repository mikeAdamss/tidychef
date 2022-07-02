#!/usr/bin/env python
# coding: utf-8

# In[1]:
from pathlib import Path

from datachef import acquire, preview, label, up, down, left, right
from datachef.selection import filters


# A simple preview
table = acquire(Path("data/bands.csv"))
preview(table)


# In[2]:


# Observation selection
obs = table.excel_ref('C4').expand(down).expand(right).is_not_blank()
preview(label(obs, "observations"))


# In[3]:


member = table.filter(filters.contains_string('John')).expand(down).is_not_blank()
preview(
    label(obs, "observations"),
    label(member, "Member")
)


# In[4]:


properties = table.excel_ref('C4:E4').fill(up).is_not_blank()
preview(
    label(obs, "observations"),
    label(member, "Member"),
    label(properties, "Properties")
)


# In[5]:


band = table.excel_ref('A1').expand(down).is_not_blank()
preview(
    label(obs, "observations"),
    label(member, "Member"),
    label(properties, "Properties"),
    label(band, "Band")
)


# In[6]:


# Shift every selection up 1
band = table.excel_ref('A1').expand(down).is_not_blank()
preview(
    label(obs.shift(up), "observations"),
    label(member.shift(up), "Member"),
    label(properties.shift(up), "Properties"),
    label(band.shift(up), "Band")
)


# In[7]:


# Shift the band selections right 3
band = table.excel_ref('A1').expand(down).is_not_blank()
preview(
    label(obs, "observations"),
    label(member, "Member"),
    label(properties, "Properties"),
    label(band.shift(right(3)), "Band")
)


# In[8]:


# Shift the band selections down
band = table.excel_ref('A1').expand(down).is_not_blank()
preview(
    label(obs, "observations"),
    label(member, "Member"),
    label(properties, "Properties"),
    label(band.spread(down), "Band")
)


# In[9]:


# Subtracting spreaded selection
band_spread_all = table.excel_ref('A1').expand(down).is_not_blank().spread(down)
band_spread_not_beatles = band_spread_all - band_spread_all.filter(filters.contains_string('Beatles'))
preview(label(band_spread_not_beatles, 'Bands spread down without beatles selected'))
