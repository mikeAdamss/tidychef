# TODO:

- pivot
- inpivot
- some DSD awareness

## Principles

**Don't** lean on pandas (it's massive, slow and constantly updated). Allow users a loosely coupled ability to leverage it, but NEVER inject it directly into the `pivoter` codebase as as dependency, save as distinct optional add-on.