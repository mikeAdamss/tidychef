# Tidychef

![Tests](https://github.com/mikeAdamss/tidychef/actions/workflows/tests.yml/badge.svg)
![100% Test Coverage](./jupyterbook/images/coverage-100.svg)
![Static Badge](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20-blue)

Tidychef is a python framework to enable “data extraction for humans” via simple python beginner friendly "recipes". It aims at allowing users to easily transform tabulated data sources that use visual relationships (human readable only data) into simple machine readable "tidy data" in a repeatable way.

i.e: it allows you to reliably turn something that looks like this: 

![](https://mikeadamss.github.io/tidychef/_images/bands-before.png)

into something that looks like this:

![](https://mikeadamss.github.io/tidychef/_images/bands-after.png)
_Note: image cropped for reasons of practicality._

Currently supported input formats are `xls`, `xlsx`, `ods` and `csv`. Though users can add additional formats relatively easily and without a codebase change being necessary.

Tidychef is **designed to allow even novice python users or analysts to quickly become productive** but also has an advanced feature set and is designed to be readily and easily extended (adding new source of tabulated data, your own use case specific methods and filters and domain specific validation etc are all possible and documented in detail).

In depth training material, examples and technical documentation [can be found here](https://mikeadamss.github.io/tidychef/intro.html#).

## Installation

```
pip install tidychef
```

## Acknowledgements

Tidychef is directly inspired by the python package [databaker](https://github.com/sensiblecodeio/databaker) created by [The Sensible Code Company](https://sensiblecode.io/) in partnership with the United Kingdoms [Office For National Statistics](https://www.ons.gov.uk/).

While I liked [databaker](https://github.com/sensiblecodeio/databaker) and successfully worked with it on multiple ETL projects over the course of almost a decade, this software should be considered the culmination of that work and the lessons learned from that time.