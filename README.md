# Tidychef

![Tests](https://github.com/mikeAdamss/tidychef/actions/workflows/tests.yml/badge.svg)
![100% Test Coverage](./jupyterbook/images/coverage-100.svg)
![Static Badge](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)

🧠 **A Different Way to Work with Tabular Data** - tidychef is built on a simple but powerful idea: **extract data the way humans interpret it — by visual structure, not by fixed positions.**

Whether your data comes from spreadsheets, CSVs, or other visually structured exports, tidychef lets you write declarative, repeatable recipes that work across inconsistent and evolving layouts.

It's designed for real-world use: publication tables, official statistics, internal reports — anything where the structure is for people, not machines.

**This isn't just a different tool. It's a different mindset.**


| 👤 You are...             | 🧩 Your problem...                                           | ✅ Tidychef helps by...                                       |
| ------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| A policy analyst          | A quarterly Excel export with merged headers and wide layout | Extracting data using visual relationships, not cell indices |
| A finance/data consultant | Repetitive report formatting with shifting structures        | Writing reusable “recipes” that adapt to visual changes      |
| A data engineer           | Need to automate legacy spreadsheets                         | Building robust, declarative extractors in Python            |


## Why use tidychef?

🧠 Visual logic — Extract data based on how it's laid out (above, beside, under), not just raw coordinates or tidy input.

🔁 Repeatable & reliable — Define logic once and reuse it across similar—but not identical—files.

💬 Beginner-friendly — Designed for analysts and non-programmers to write recipes in simple Python.

📦 Interoperable — Outputs tidy pandas DataFrames or CSVs, ready for analysis in Python or R.

🧱 Built for real-world data — Handles spreadsheets with multi-level headers, merged cells, footnotes, and visual groupings that traditional tools struggle with.

🧑‍💼 Built for—and with—real data practitioners

📈 Robust to evolving layouts: Rather than relying on fixed coordinates, tidychef locates data by interpreting spatial relationships, allowing your extraction scripts to flexibly handle new or shifted data.

## Basic Example

💡 Note: This example is intentionally simple — a clear demonstration of tidychef’s core concept.
tidychef excels at extracting data from highly irregular, human-readable, and widely inconsistent spreadsheets (or other tabulated sources) — the kinds of things that break conventional tools.

This example shows how to extract asset ownership data from a spreadsheet with multi-level column headers and repeating row groups — a layout that often challenges traditional tools or adds burdensome complexity.

Imagine a sheet where relationships between cell values are primarily expressed spatially, not just by position.

![](https://mikeadamss.github.io/tidychef/_images/bands-before.png)

You write a fairly concise script

```python
from tidychef import acquire, filters, preview
from tidychef.direction import right, below
from tidychef.output import TidyData, Column

# Load a CSV table from a URL
table = acquire.csv.http("https://raw.githubusercontent.com/mikeAdamss/tidychef/main/tests/fixtures/csv/bands-wide.csv")

# Select numeric observations and label them
observations = table.filter(filters.is_numeric).label_as("Value")

# Label headers based on their positions
bands = table.excel_ref("3").is_not_blank().label_as("Band")
assets = table.excel_ref("2").is_not_blank().label_as("Asset")
names = table.excel_ref("A4").expand(right).expand(down).filter(filters.is_not_numeric).is_not_blank().label_as("Name")
preview(observations, bands, assets, names)

# Build tidy data by associating observations with their corresponding headers
tidy_data = TidyData(
    observations,

    # "Band" labels are closest to the right of each value
    Column(bands.finds_observations_closest(right)),

    # "Assets" labels are directly below each value
    Column(assets.finds_observations_directly(below)),
    
    # "Names" labels are direcrly to the right of each value
    Column(names.finds_observations_directly(right))
)

# Export the tidy data to CSV
tidy_data.to_csv("bands_tidy.csv")

```

which make will get you an inline preview (because we used `preview()` in the snippet)

![preview](./preview1.png)

and will putput a csv (`band_tidy.csv` as per the snippet) that looks like this:

![](https://mikeadamss.github.io/tidychef/_images/bands-after.png)
_Note: image cropped for reasons of practicality._


💡 💡 **KEY INSIGHT** 💡💡

This is the bit you need to understand above all -here’s a preview I've made from tunn **the exact same script** against a _radically altered data source_. This is what we mean by _robust_ and _repeatable_ transforamations and why the focus of tidychef is modeling spatial relationships — how cells relate visually, not where they are.

💡 Same script, radically different input—same output.

![preview](./preview2.png)

Even when data changes (as it will if you're working with any kind of regular publication) the _spatial relationships_ rarely change and typically only in ways that can be accounted for with a little care.

## More Info

Currently supported input formats are `xls`, `xlsx`, `ods` and `csv`. Though users can add additional formats relatively easily and without a codebase change being necessary.

Tidychef is **designed to allow even novice python users or analysts to quickly become productive** but also has an advanced feature set and is designed to be readily and easily extended (adding new source of tabulated data, your own use case specific methods and filters and domain specific validation etc are all possible and documented in detail).

Extensive [training materials, examples and technical documentation can be found here](https://mikeadamss.github.io/tidychef/intro.html#).

## Installation

```
pip install tidychef
```

## Acknowledgements

Tidychef is directly inspired by the python package [databaker](https://github.com/sensiblecodeio/databaker) created by [The Sensible Code Company](https://sensiblecode.io/) in partnership with the United Kingdoms [Office For National Statistics](https://www.ons.gov.uk/).

While I liked [databaker](https://github.com/sensiblecodeio/databaker) and successfully worked with it on multiple ETL projects over the course of almost a decade, this software should be considered the culmination of that work and the lessons learned from that time.