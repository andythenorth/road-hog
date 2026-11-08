#!/usr/bin/env python3
"""Audit visible-cargo end-state without asserting unsupported feature parity."""

# CABBAGE: after Step 018 renames the strategy/template, earlier migration scripts
# are historical steps and must not reapply transformations to the old contracts.
from pathlib import Path as _visible_cargo_migration_path
if (
    _visible_cargo_migration_path("src/templates/vehicle_with_precomposited_cargo.pynml").is_file()
    and not _visible_cargo_migration_path("src/templates/vehicle_with_visible_cargo.pynml").exists()
    and "class GestaltGraphicsPrecompositedCargo"
    in _visible_cargo_migration_path("src/gestalt_graphics/gestalt_graphics.py").read_text(encoding="utf-8")
):
    print("Earlier visible-cargo step superseded by Step 018 rename")
    raise SystemExit(0)


import ast
from pathlib import Path

STRATEGY = Path("src/gestalt_graphics/gestalt_graphics.py")
PIPELINE = Path("src/gestalt_graphics/pipelines.py")
TEMPLATE = Path("src/templates/vehicle_with_visible_cargo.pynml")
UNITS = Path("src/road_vehicle/units.py")


def methods_in_class(path, name):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    matches = [
        node
        for node in tree.body
        if isinstance(node, ast.ClassDef) and node.name == name
    ]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one {name} in {path}")
    return {
        node.name for node in matches[0].body if isinstance(node, ast.FunctionDef)
    }


def main():
    for path in (STRATEGY, PIPELINE, TEMPLATE, UNITS):
        if not path.is_file():
            raise SystemExit(f"Run from repository root: missing {path}")
    strategy = STRATEGY.read_text(encoding="utf-8")
    pipeline = PIPELINE.read_text(encoding="utf-8")
    template = TEMPLATE.read_text(encoding="utf-8")
    methods = methods_in_class(STRATEGY, "GestaltGraphicsVisibleCargo")
    needed = {
        "get_output_row_types",
        "get_unique_spritesets",
        "get_output_row_count_for_unit",
        "get_spriterow_types_for_units",
    }
    if missing := needed - methods:
        raise RuntimeError(f"Missing visible-cargo methods: {sorted(missing)}")
    if "sorted(set(row_nums_seen))" not in strategy:
        raise RuntimeError("Non-deterministic cargo row enumeration")
    if "get_output_row_count_for_unit(" not in strategy:
        raise RuntimeError("Unit row counting missing")
    if "get_unique_spritesets(unit)" not in template:
        raise RuntimeError("Template does not use spriteset enumeration")
    if "get_spriteset_template_name(" not in template:
        raise RuntimeError("Template bypasses unit spriteset interface")
    if "get_spriterow_types_for_model(consist)" not in pipeline:
        raise RuntimeError("Pipeline does not use gestalt-provided row types")
    if "Unsupported compositor row type" not in pipeline:
        raise RuntimeError("Pipeline dispatch is not exhaustive")
    if "def get_spriteset_template_name(" not in UNITS.read_text(encoding="utf-8"):
        raise RuntimeError("Unit spriteset interface missing")

    print("Step 017: supported visible-cargo interfaces and callers PASS")
    print("Deferred, not asserted as Iron Horse parity:")
    print("- Road Hog source-row geometry and fixed-row articulated units")
    print("- Covered-body and multiple-weathering compositor support")
    print("- Per-unit spriteset-template naming and purchase sprites")
    print("- Other graphics strategies using shared legacy row-count methods")
    print("Full make / GRF production requires repository verification")


if __name__ == "__main__":
    main()
