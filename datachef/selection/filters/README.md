# Filters

Filters are stand alone callables that return a boolean value when given a parameter of a single cell. As an example `contains_string("foo")` is a filter that that will return `True` if a cells value contains the text "foo", else it will return `False`.

example:
```python
# select all cells in a table with a cell value containing "foo"
selection = table.filter(contains_string("foo"))
```

Filters are intended to be passed as parametes to the `Selection.filter()` method.

Filters are largely interchangable so the submodules are just used as a convienient way to categorise them by purpose.

## Why filters and not methods?

So I could have offered up the `contains_string` example as `table.contains_string("foo")` easily enough and I'll admit to being tempted, but there' a subtle design distinction here:

The filters operate on the _contents_ of the cell(s), whereas the methods tend to operate on the properties of the cell (i.e their positioning on the x and y axis).

I will admit that's not exhaustive nor is intended to be, for example I have exposed some of the very common content operations as methods for user convenience (eg: `is_blank()`) but on the whole it's a distinction I'd like to keep to.

More importantly I'm envisioning filters as more a community resource, as their decoupled enough from the flow of the code that (assuming decent naming, documentation and some tests) new ones can be merged into datachef fairly casually without risk of overwhelming users with options they may very well never use.

**Design Note:**

For the purpose of keeping the API consistant and user friendly, we'll be aliasing the
filters that are classes to snake case during export, so `ContainsString` will to exposed as `contains_string`.

I'm aware that the former is more pythonic, but this tool is aimed squarely at analysts as much or more so than programmers and consistentency between the class and function based filters is important to our primary "make it as easy to use as possible" goal.


