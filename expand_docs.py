"""
Simple script to add some dynamic elements to our documentation.

Principally by adding links to the html output of our scenarios to
the techical documentation (so a browsing user can easily view
the behaviour were confirming per build).
"""

from os import linesep
from pathlib import Path

this_dir = Path(__file__).parent
raw_splashpage = Path(this_dir / "_docs" / "raw_splashpage.md")
splashpage = Path(this_dir / "_docs" / "splashpage.md")

with open(raw_splashpage) as f:
    page_lines = f.readlines()

scenarios = Path(this_dir / "scenarios" / "expected").glob("*.html")
assert len(list(scenarios)) > 0, "No scenarios found, aborting build."
for scenario in scenarios:
    page_lines.append(
        f"- https://mikeadamss.github.io/datachef/{scenario.name}{linesep}"
    )

with open(splashpage, "w") as f:
    f.writelines(page_lines)
