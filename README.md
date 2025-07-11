# Tidychef

![Tests](https://github.com/mikeAdamss/tidychef/actions/workflows/ci.yml/badge.svg)
![100% Test Coverage](./jupyterbook/images/coverage-100.svg)
![Static Badge](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)

🧠 **A Different Way to Work with Tabular Data**

Tidychef is a Python tool that helps you extract data from **human-oriented spreadsheets**—the kind published by governments, NGOs, and analysts.

Rather than relying on rigid cell references, Tidychef lets you define **spatial relationships** like “this value is below this header,” or “shift right from here,” making your scripts repeatable even when layouts evolve.

> 📊 _Built for real-world publication tables: ONS, NHS, DfE, local authority reports, and more._


## 👥 Who Is Tidychef For?


| 👤 You are...             | 🧩 Your problem...                                           | ✅ Tidychef helps by...                                       |
| ------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| A policy analyst          | A quarterly Excel export with merged headers and wide layout | Extracting data using visual relationships, not cell indices |
| A finance/data consultant | Repetitive report formatting with shifting structures        | Writing reusable “recipes” that adapt to visual changes      |
| A data engineer           | Need to automate legacy spreadsheets                         | Building robust, declarative extractors in Python            |

> [AI-powered overview](https://mikeadamss.github.io/tidychef/ai-overview): See how tidychef compares to other tools.


## 📊 Example

Consider this Excel-like structure — built for readers, not for code.

![](https://mikeadamss.github.io/tidychef/_images/bands-before.png)

A simple script

```python
from tidychef import acquire, filters, preview
from tidychef.direction import down, right, below
from tidychef.output import Column, TidyData

# Load a CSV table from a URL
table = acquire.csv.http(
    "https://raw.githubusercontent.com/mikeAdamss/tidychef/main/tests/fixtures/csv/bands-wide.csv"
)

# Select numeric observations and label them
observations = table.is_numeric().label_as("Value")

# Select headers and label them
bands = table.row_containing_strings(["Beatles"]).is_not_blank().label_as("Band")
assets = table.row_containing_strings(["Cars"]).is_not_blank().label_as("Asset")
names = table.cell_containing_string("Beatles").shift(down).expand_to_box().is_not_numeric().label_as("Name")

# We'll request a preview to see our selections
preview(observations, bands, assets, names)

# Build tidy data by attaching observations and headers
tidy_data = TidyData(
    observations,
    Column(bands.attach_closest(right)),
    Column(assets.attach_directly(below)),
    Column(names.attach_directly(right)),
)

# Export the tidy data to CSV
tidy_data.to_csv("bands_tidy.csv")
```

which will get you an inline preview (because we used `preview()` in the snippet)

![preview](./docs/preview1.png)

and will putput a csv (`band_tidy.csv` as per the snippet) that looks like this:

![](https://mikeadamss.github.io/tidychef/_images/bands-after.png)
_Note: image cropped for reasons of practicality._


💡 💡 **KEY INSIGHT** 💡💡

This is the bit you need to understand above all - here’s another preview I've made from running **the exact same script** against a _radically altered version of the data source_. This is what we mean by _robust_ and _repeatable_ transformations and why the focus of tidychef is modeling spatial relationships — how cells relate visually.

💡 Same script, radically different input—same output structure.

![preview](./docs/preview2.png)

📌 You’re modeling visual structure, not fixed coordinates!


## 🔍 Why Use Tidychef?

🧠 Visual logic — Work like a human, not like a parser.

🔁 Repeatable recipes — Robust to changes in layout, column order, or row spacing.

📦 Tidy output — Standard pandas.DataFrame or CSV.

🤝 Beginner-friendly — Analysts can learn fast with real-world examples.

🛠️ Advanced extensibility — Developers can subclass, extend, and customize as needed.


## 📘 Full Documentation

Extensive documentation, including tutorials, real UK government datasets, advanced recipes, and developer guidance is available at:

👉 [mikeadamss.github.io/tidychef](https://mikeadamss.github.io/tidychef/index.html)


## Installation

```
pip install tidychef
```

## Acknowledgements

Tidychef is directly inspired by the python package [databaker](https://github.com/sensiblecodeio/databaker) created by [The Sensible Code Company](https://sensiblecode.io/) in partnership with the United Kingdoms [Office For National Statistics](https://www.ons.gov.uk/).

While I liked [databaker](https://github.com/sensiblecodeio/databaker) and successfully worked with it on multiple ETL projects over the course of almost a decade, I do consider this software the culmination of that work and the lessons learned from that time.

## Get Involved

Please raise issues (or ideas as issues) freely on this repo.

If you'd like to get involved more directly then please see [contributing](./docs/CONTRIBUTING.md) guidance.
