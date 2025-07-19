This document is just an informal holding ground for some thoughts that are baking but aren't quite ready to come out of oven yet. I might add them, I might not. If you're reading this consider anything you see as notes for the future and strictly possibilties not promises.

i.e I had an interesting thought while doing something else so scribbled it down here. As such these are notes to self and should not be confused with documentation, or indeed even a good or properly thought through idea.

**Important - everyting here is informal and speculative and in no way a promise of anything that'll actually happen**

## Do better examples

The examples are all fine but with could probably all be cleaner and I'd like more. The less cognitive load in onboarding the better, we want people up and using tidychef in seconds not minutes. 

## Interactive demo

There are a few soltions for sharing runable code, including notebooks. Would it be good to share a runable example with people?

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
selction.expand(right, until=is_numeric)
```

i.e expand right but stop expanding on a given row when you hit a condition, i.e is_numeric, is_blank, is_row(2), is_column("D"), contains_str("foo") etc etc

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


## Sweep

Similar to table block, there's potentially a repeating sceanrio where there are lots of occasions where we want to largely grab everyting relative to a cardinal direction from a single point, so effectively

```
<single cell selection>.sweep(right)

# could be a  nice proxy/wrapper for ...

<single cell selection>.expand(right).expand(down).expand(up).is_not_blank()
```

and possibly

```
<single cell selection>.sweep(right, include_blanks=True)

# could be a  nice proxy/wrapper for ...

<single cell selection>.expand(right).expand(down).expand(up)
```

it _feels_ like could potentially simplify a lot of recipes but (a) "sweep" doesn't quite capture the behavioud and (b) it could bequite unintuitive to "sweep" from multiple points, wemight to enforce the single cell starting point which would need careful conventions and handling to be obvious.

## Raise for emply Selector returns

I cant see any reason why any Selectable method that reults in 0 selectec cells would be desirable. Should we just raise when this happens? That feels like it'd make debugging easier. 

Maybe a decorator, i.e _something_ like `@ensure_has_cells`.

_think this one through_, it feels right but it'd be very abolsute by its nature.

## Label Previews

It would be nice if people could optionally provide a label/heading for previews.This woulebehandy with multi preview / itertive extraction sceanrios.

## Google Sheets

An acquire mechanism for google sheets feels likean easy win, just put some thought into auth, need it to be an implementation that's equally accessible to the less technical folks.

Have a think on api pattern:

```
acquire.sheets.http() ?
acquire.google.http() ?

# more interestingly
acquire.google.sheets.http?
# thats verbose ..but.. there are all sorts of google offerings that you could imbibe as a table, might be worth it, have a mull
# ...but is there a non http google sheet? does it matter?
```