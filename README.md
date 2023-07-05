# Datachef

![The test coverage for datachef is 100%](./coverage-100.svg)

> :warning: This software is a **work in progress**. Documentation thus far can be viewed at: https://mikeadamss.github.io/datachef/datachef.html#datachef

Datachef is a pet/passion project to create a ground up rewrite and extension of the functionality of https://github.com/sensiblecodeio/databaker. 


## Makefile

A `Makefile` is included to streamline some recurring developments tasks. Running a naked `make` from the command line will display a simple help menu.

_Note: Mac and most Linux distributions have Make by default, windows as I understand it would require a bit of work._

---

## Development

TODO

---

## Building Documentation

API documentation is build automatically with [pdoc](https://pdoc.dev/) then supplemented with static assets from `_docs`.

This is done automatically on git merge and can be done locally (for previewing changes) via the included `Makefile`.
