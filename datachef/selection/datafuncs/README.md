# Datafunctions

Datafunctions are stand alone functions that operate on basic cell (typically `BaseCell`) or primitve python variables.

These functions power the methods in use by the variations of the `Selectable` class.

This is a design choice to keep the api user friendly but also allow for more advanced users to dip into the data dunctions directly to deal with unexpected and/or advanced use cases.

All submodules are imported with `datafuncs`, the separation is for convenience and categorisation while developing. 