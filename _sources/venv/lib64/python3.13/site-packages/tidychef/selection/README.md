# Selection

The selection module holds two distinct submodules that define how you conditional create and modify selections of cells taken from a given tabulated data source.

`selects` - Holds and defines the base `Selection' class. This object is the principle way a user will interact with tabulated data.

`datafuncs` - The low level functions that power the aforementioned `Selection` class and any format specfic selection classes that inherit from it.