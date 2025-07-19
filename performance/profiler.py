import cProfile
import csv
import importlib.util
import pstats
import subprocess
from datetime import datetime
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent / "scripts"
CSV_PATH = Path(__file__).parent / "results.csv"


def get_git_commit():
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return "unknown"


def run_recipe_module(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if hasattr(module, "main"):
        # Expecting three timedelta values
        return module.main()
    else:
        raise RuntimeError(f"Script {path} has no main() function.")


def profile_recipe(recipe_path):
    profiler = cProfile.Profile()
    profiler.enable()

    acquire, selection, transform, observations = run_recipe_module(recipe_path)

    profiler.disable()
    stats = pstats.Stats(profiler).strip_dirs().sort_stats("cumtime")

    total_calls = sum(call[0] for call in stats.stats.values())
    primitive_calls = sum(call[1] for call in stats.stats.values())
    total_time = stats.total_tt
    avg_time_per_call = total_time / total_calls if total_calls else 0

    return {
        "name": recipe_path.name,
        "total_time": total_time,
        "total_calls": total_calls,
        "primitive_calls": primitive_calls,
        "avg_time_per_call": avg_time_per_call,
        "acquire_time": acquire.total_seconds(),
        "selection_time": selection.total_seconds(),
        "transform_time": transform.total_seconds(),
        "observations_extracted": observations,
    }


def write_result_to_csv(result, commit_hash):
    is_new = not CSV_PATH.exists()

    with CSV_PATH.open("a", newline="") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(
                [
                    "Date",
                    "Commit",
                    "Script",
                    "CPU Time (s)",
                    "Calls",
                    "Prim Calls",
                    "Avg Time/Call (ms)",
                    "Acquire Time Total (s)",
                    "Selection Time Total (s)",
                    "Transform Time Total (s)",
                    "Observations Extracted",
                    "Time Per Observation Extracted (s)",
                ]
            )

        writer.writerow(
            [
                datetime.utcnow().isoformat(),
                commit_hash,
                result["name"],
                f"{result['total_time']:.4f}",
                result["total_calls"],
                result["primitive_calls"],
                f"{result['avg_time_per_call'] * 1000:.4f}",
                f"{result['acquire_time']:.4f}",
                f"{result['selection_time']:.4f}",
                f"{result['transform_time']:.4f}",
                result["observations_extracted"] - 1,  # Subtract 1 for the header row
                (
                    result["acquire_time"]
                    + result["selection_time"]
                    + result["transform_time"]
                )
                / (result["observations_extracted"] - 1),
            ]
        )


def main():
    recipe_files = sorted(SCRIPTS_DIR.glob("*.py"))
    commit_hash = get_git_commit()

    print("\nProfiling recipes...\n")
    for recipe_path in recipe_files:
        print(f"Profiling {recipe_path.name} ...")
        result = profile_recipe(recipe_path)
        write_result_to_csv(result, commit_hash)

    print("\nResults appended to", CSV_PATH.name)


if __name__ == "__main__":
    main()
