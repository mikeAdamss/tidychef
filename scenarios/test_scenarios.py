import os
import shutil
from os import linesep
from pathlib import Path


## Get html output of all raw .py notebooks
def test_all_notebooks():
    """
    Test that all notebooks included in ./scenarios create the
    expected output as shown in ./expected
    """

    this_dir = Path(__file__).parent

    created_dir = Path(this_dir / "created")
    if created_dir.exists():
        shutil.rmtree(created_dir)
    created_dir.mkdir()

    scenario_dir = Path(this_dir / "scenarios")
    expected_dir = Path(this_dir / "expected")

    for scenario in scenario_dir.glob("./*.py"):

        # Create notebook from python file
        os.system(f"jupytext --to notebook {scenario.resolve()}")

        # Run that notebook
        path_to_notebook = Path(str(scenario.resolve()).replace(".py", ".ipynb"))
        os.system(
            f"jupyter-nbconvert --to html --output-dir='{created_dir.resolve()}' --ExecutePreprocessor.timeout=None --execute '{path_to_notebook}'"
        )

        html_name = str(path_to_notebook.name).replace(".ipynb", ".html")

        new_output = list(created_dir.glob(f"./{html_name}"))[0]
        old_output = list(expected_dir.glob(f"./{html_name}"))[0]

        with open(new_output) as f1:
            with open(old_output) as f2:
                assert f1.read() == f2.read(), (
                    f"Unexpected output:{linesep}"
                    f"- the new output : {new_output.resolve()}{linesep}"
                    f"- created from   : {scenario.resolve()}{linesep}"
                    f"- does not match : {old_output.resolve()}{linesep}"
                )
