"""
We'd rather avoid storing large amound of .html and .ipynb in github but we use
significant numbers of both for running unit tests and scenarios.

The bundler zips or unzips these resources and places them in the relevant places.

NOTE: the targets dirs for unzipping are all locations specified in the gitignore,
please continue this practice if you add more locations.
"""

import shutil
import sys
from pathlib import Path

# Inputs
repo_base = Path(__file__).parent.parent
scenario_dir = Path(repo_base / "scenarios")
screnarios_created_dir = Path(scenario_dir / "created")
resource_dir = Path(repo_base / "resources")

# Ipynb checkpoints, we dont want to store them
checkpoints_to_remove = [
    Path(scenario_dir / ".ipynb_checkpoints"),
    Path(scenario_dir / "html_scenario_fixtures" / ".ipynb_checkpoints"),
]

# Outputs
scenarios_storage_path = Path(resource_dir / "scenarios")


def bundle():
    """
    A function to bundle (zip) the .html and .ipynb resources
    used for testing.
    """

    # Make sure we have our expected subject directories
    assert scenario_dir.exists(), (
        "Cannot bundle scenarios directory as no scenario "
        "directory currently exists."
    )

    # remove the created dir from scenarios if present, these are ephemeral files
    if screnarios_created_dir.exists():
        shutil.rmtree(screnarios_created_dir)

    # remove ipynb checkpoint dirs
    for ckpoint_path in checkpoints_to_remove:
        if ckpoint_path.exists():
            shutil.rmtree(ckpoint_path)

    # bundle up the scenarios dir
    shutil.make_archive(scenarios_storage_path, "zip", scenario_dir)


def unbundle():
    """
    A function to unbundle (unzip) the .html and .ipynb resources
    used for testing and place them in the appropriate places
    """

    import zipfile

    with zipfile.ZipFile(f"{scenarios_storage_path.resolve()}.zip", "r") as zip_ref:
        zip_ref.extractall(scenario_dir)


if __name__ == "__main__":
    if sys.argv[1] == "bundle":
        bundle()
    elif sys.argv[1] == "unbundle":
        unbundle()
    else:
        raise ValueError(
            "The first argument to the bundler must be either bundle"
            f" or unbundle, got {sys.argv[1]}"
        )
