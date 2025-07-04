Tidychef has a pretty strong api but there's a lot I'd like to add.

This document is just an informal holding ground for some thoughts that are baking but aren't quite ready to come out of oven yet. I might add them, I might not. If you're reading this consider anything you see as notes for the future and strictly possibilties not promises.

**i.e everyting here is speculative!!**

## Contiguous Cell Propositions

Note, we need a _waaay_ snappier way of describing this before it gets anywhere near the api.

One of the big untapped visual clues we've not wrapped in a convenient method is "get cells similar to the ones we've already got" there's things to figure our but that feels like a massive value add. Think roughly _something_ (not this, but like this) like:

```
selection.where_has_neighbour([ABOVE, BELOW], is_numeric)
```

so - get me all cells that have a cell with a number above it or below it. That feels like it could sweep up observations and dodge any conicidental cells (footer notes etc) that might just so happen to be numeric. 

if you think of header rows, somethign like this:

```
selection.where_has_neighbour([LEFT, RIGHT], is_not_numeric)
```

possibly even

```
selection.where_has_neighbour([LEFT, RIGHT], is_not_numeric, minimum_viable_len=4)
```

i.e - get me a selection of cells, made of of a horizontal presentation of stings but only where we end up with a selection of at least 4.

...feels... like it _might_ be fairly powerful. Quite a lot of title rows consist of horizontal sequences of cells, it _could_ move us closer to "give me the header - wherever they are, I don't care to specify more than that". 


## until

...this needs more though, but some of of generic `until` kwarg that can make other methods (particular methods that are analgous to mouse selections) operate via some sort of shared but obvious "do until" approach feels worth exploring.

so _something_ like:

```
selction.expand(right, until=not(str))
```

i.e expand right but stop expanding on a given row when you hit number or blank.

## Cell Formatting

The whole point of `Selectable` was to allow per file format handling which gives us an entry point for selection based in styling, so by way of a simple example:

```
selection.is_bold()
selection.is_underlined()
# with _not_ versions ofc
```

is totally viable, you'd just have a different implementation for `XlsSelectable` vs `XlsxSelectable`, we've got a clear point of intervention for doing this.

we ...probably... want a shared spreadsheet base class so we can enforece some sort of inheritance to avoid too much divergence, i.e right now its:

```
-> Selectable -> XlsSelectable
```

we _maybe, unsure, consider_ we want something a bit more like:

```
-> Selectable -> FormatableSelectable -> XlsSelectable
```

basically consider putting `_is_bold()` on all children of FormatableSelectable in an enforcable way. Having `is_bold()` as an option on _those formats that have bold_ is fine and shouldn't confuse anyone (nobodies gonna try and find the bold cell in a csv).But I don't want to mix and match, that'll fragment the api too much.

in fact .....maybe.... we put an `is_bold()` on `Selectable` and raise a "format x doesn't do bold cells" type error in case of lazy cut and paste confusion for users. If `FormatableSelectable` forces the child to override if that should help keep us honest.

## Consider removing explain=

It doesn't feel like something someone would use all that much once they've got a grip on the api. Wait and see but (unless we need other config options) it might not be worth having.


## Table block

We seem to do a lot of:

- go to a cell
- expand(right)
- expand(down)
- is_not_blank()

which makes sense, most sheets have a solid rectangular block of values or two we need to sweep up, so we can make this a lot easier?

i.e

```
observations = selection.from_corner_cell(<one selected cell>)  # note, name needs thought
```

Humans read left to right and up to down so we naturally always start at the top left of a rectangular-ish block of values, so can it literally just be this clean?