"""
Quick and dirty profiler for tidychef recipes.
"""

import cProfile
import importlib.util
import pstats
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent / "scripts"


def run_recipe_module(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if hasattr(module, "main"):
        module.main()
    else:
        raise RuntimeError(f"Script {path} has no main() function.")


def profile_recipe(recipe_path):
    profiler = cProfile.Profile()
    profiler.enable()

    run_recipe_module(recipe_path)

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
    }


def main():
    recipe_files = sorted(SCRIPTS_DIR.glob("*.py"))
    results = []
    for recipe_path in recipe_files:
        print(f"Profiling {recipe_path.name} ...")
        result = profile_recipe(recipe_path)
        results.append(result)

    print("\nPerformance summary:")
    print(
        f"{'Script':30s} | {'CPU Time (s)':>12s} | {'Calls':>8s} | {'Prim Calls':>10s} | {'Avg Time/Call (ms)':>18s}"
    )
    print("-" * 90)
    for r in results:
        print(
            f"{r['name']:30s} | {r['total_time']:12.4f} | {r['total_calls']:8d} | {r['primitive_calls']:10d} | {r['avg_time_per_call']*1000:18.4f}"
        )

    import shutil

    shutil.rmtree("data.csv", ignore_errors=True)  # Clean up any generated data files


if __name__ == "__main__":
    main()
