"""
Simple script to add some dynamic elements to our documentation.

Principally by adding links to the html output of our scenarios to
the techical documentation (so a browsing user can easily click into
and view the html output of the scenarios.
"""

from os import linesep
from pathlib import Path

this_dir = Path(__file__).parent
raw_splashpage = Path(this_dir / "_docs" / "raw_splashpage.md")
splashpage = Path(this_dir / "_docs" / "splashpage.md")

with open(raw_splashpage) as f:
    page_lines = f.readlines()

scenarios = Path(this_dir / "scenarios" / "html_scenario_fixtures").glob("*.html")
scenario_file_list = list([x.name for x in scenarios])
print(scenario_file_list)
assert (
    len(list(scenario_file_list)) > 0
), "No scenarios found, aborting build. Have you ran 'make unbundle?'"
for scenario in scenario_file_list:
    page_lines.append(f"[{scenario}](/{scenario}){linesep}")

with open(splashpage, "w") as f:
    for line in page_lines:
        f.write(line + linesep)
