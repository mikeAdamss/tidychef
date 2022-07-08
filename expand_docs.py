"""
Simple script to add some dynamic elements to our documentation
"""

from os import linesep
from pathlib import Path

this_dir = Path(__file__).parent

raw_splashpage = Path(this_dir / "_docs" / "raw_splashpage.md")
splashpage = Path(this_dir / "_docs" / "splashpage.md")

with open(raw_splashpage) as f:
    page_lines = f.readlines()

scenario_dir = Path(this_dir / "scenarios" / "expected").glob("*.html")
for scenario in scenario_dir:
    page_lines.append(
        f"* https://mikeadamss.github.io/datachef/{scenario.name}{linesep}"
    )

with open(splashpage, "w") as f:
    f.writelines(page_lines)
