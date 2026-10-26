#!/usr/bin/env python3
"""Move compositor row-type dispatch to the Iron Horse-style string contract.

Retain Road Hog source-offset arithmetic and graphics composition unchanged.
"""

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

STRATEGY_PATH = Path("src/gestalt_graphics/gestalt_graphics.py")
PIPELINE_PATH = Path("src/gestalt_graphics/pipelines.py")

OLD_STRATEGY = """    def get_legacy_road_hog_output_row_groups(self, units):
"""
NEW_STRATEGY = """    def get_spriterow_types_for_units(self, units):
        # The compositor consumes row types, as in Iron Horse. Retain the
        # unit-specific fixed-row distinction until its graphics migrate.
        return [
            [row_type for row_type, _ in unit_rows]
            for unit_rows in self.get_legacy_road_hog_output_row_groups(units)
        ]

"""
OLD_PIPELINE = """    def get_legacy_road_hog_spriterows_for_consist(self, legacy_consist):
        # CABBAGE: the pipeline still consumes tuple descriptors rather than
        # Iron Horse row types; the graphics strategy now owns their selection.
        return legacy_consist.gestalt_graphics.get_legacy_road_hog_output_row_groups(
            legacy_consist.unique_units
        )
"""
NEW_PIPELINE = """    def get_spriterow_types_for_model(self, model_variant):
        return model_variant.gestalt_graphics.get_spriterow_types_for_units(
            model_variant.unique_units
        )
"""
OLD_LOOP = """            self.get_legacy_road_hog_spriterows_for_consist(consist)
"""
NEW_LOOP = """            self.get_spriterow_types_for_model(consist)
"""
OLD_TYPE = """                spriterow_type = spriterow_data[0]
"""
NEW_TYPE = """                spriterow_type = spriterow_data
"""


def replace_once(source, old, new, label):
    if old in source:
        if source.count(old) != 1:
            raise RuntimeError(f"Ambiguous {label}")
        return source.replace(old, new, 1)
    if new in source:
        return source
    raise RuntimeError(f"Unexpected source layout for {label}; refusing to edit")


def main():
    for path in (STRATEGY_PATH, PIPELINE_PATH):
        if not path.is_file():
            raise SystemExit(f"Run from repository root: missing {path}")

    original = {
        path: path.read_text(encoding="utf-8")
        for path in (STRATEGY_PATH, PIPELINE_PATH)
    }
    strategy = original[STRATEGY_PATH]
    if NEW_STRATEGY not in strategy:
        if strategy.count(OLD_STRATEGY) != 1:
            raise RuntimeError("Legacy row-group method missing or ambiguous")
        strategy = strategy.replace(OLD_STRATEGY, NEW_STRATEGY + OLD_STRATEGY, 1)

    pipeline = original[PIPELINE_PATH]
    pipeline = replace_once(pipeline, OLD_PIPELINE, NEW_PIPELINE, "row-type interface")
    pipeline = replace_once(pipeline, OLD_LOOP, NEW_LOOP, "compositor row iterator")
    pipeline = replace_once(pipeline, OLD_TYPE, NEW_TYPE, "row-type dispatch")
    pipeline = replace_once(
        pipeline,
        """        for vehicle_counter, vehicle_rows in enumerate(
            self.get_spriterow_types_for_model(consist)
        ):
            # !! ^ this is ugly hax, I didn't want to refactor the iterator above to contain the vehicle, also in Horse
""",
        """        for vehicle_counter, vehicle_rows in enumerate(
            self.get_spriterow_types_for_model(consist)
        ):
""",
        "obsolete iterator comment",
    )

    changes = {STRATEGY_PATH: strategy, PIPELINE_PATH: pipeline}
    for path, source in changes.items():
        ast.parse(source, filename=str(path))
    for path, source in changes.items():
        if source != original[path]:
            path.write_text(source, encoding="utf-8")
            print(f"Updated {path}")
    print("Step 010: compositor consumes row-type names, retaining source offsets")


if __name__ == "__main__":
    main()
