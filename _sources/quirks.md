# Quirks

The following page contains some quick notes on quirks of tidychef that might throw a first time user.


## Excel references

Regardless of the format in question tidychef makes heavy use of the phrase "excel reference" or more commonly `excel_ref()`.

This is **nothing** to do with excel or even spreadsheets, it's simply a matter of practicality.

If you say "excel reference C3" the vast majority of people will know what you are talking about. If you say "x offset 2, y offset 4" you've just lost half the audience. We prefer to keep things accessible to the majority.

This will mean an odd moment the first time you `excel_ref()` some csv data, but just remember its an _excel **style** reference_.

Along the same lines, its `excel_ref()` not `spreadsheet_ref()` for simple reasons of brevity.