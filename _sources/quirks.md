# Quirks

The following page contains some quick notes on quirks of datachef that might throw a first time user.


## Not everyone is a programmer

Datachef is aimed at analysts, data engineers and relative newcomers to python as much and probably more than its aimed at experienced python developers and the style of this documentation reflects that.

As such, the experienced programmers amongst you may find some of the explanations teeth grindingly simplified and lacking in more complex technical explanation and discussion.

Rest assured, this is a conscious choice based on our target audience.


## Excel references

Regardless of the format in question datachef makes heavy use of the phrase "excel reference" or more commonly `excel_ref()`.

This is **nothing** to do with excel or even spreadsheets, it's simply a matter of practicality.

If you say "excel reference C3" the vast majority of people will know what you are talking about. If you say "x offset 2, y offset 4" you've just lost half the audience. We prefer to keep things accessible to the majority.

This will mean an odd moment the first time you `excel_ref()` some csv data, but just remember its an _excel **style** reference_.

Along the same lines, its `excel_ref()` not `spreadsheet_ref()` for simple reasons of brevity.