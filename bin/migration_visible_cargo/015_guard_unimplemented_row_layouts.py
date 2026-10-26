#!/usr/bin/env python3
"""Guard unsupported visible-cargo rows and use the shared row-height constant."""

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
GUARD = """        # CABBAGE: the Road Hog compositor does not yet emit covered or multiple weathering rows.
        if self.covered_vehicle_body:
            raise NotImplementedError(
                "Visible-cargo covered_vehicle_body requires compositor migration"
            )
        if len(self.weathered_states) != 1:
            raise NotImplementedError(
                "Visible-cargo multiple weathered_states require compositor migration"
            )
"""


def main():
    if not STRATEGY.is_file():
        raise SystemExit(f"Run from repository root: missing {STRATEGY}")
    original = STRATEGY.read_text(encoding="utf-8")
    text = original
    constructor_end = """        self.weathered_states = kwargs.get(
            "weathered_states", {"unweathered": self.body_recolour_map}
        )
"""
    if GUARD not in text:
        if text.count(constructor_end) != 1:
            raise RuntimeError("Unexpected visible-cargo constructor: not modifying source")
        text = text.replace(constructor_end, constructor_end + GUARD, 1)
    old = """                    start_y_cumulative + 30,
"""
    new = """                    start_y_cumulative + row_height,
"""
    if old in text:
        if text.count(old) != 1:
            raise RuntimeError("Unexpected loaded-row offset count")
        text = text.replace(old, new, 1)
    elif new not in text:
        raise RuntimeError("Unexpected loaded-row offset expression")
    ast.parse(text, filename=str(STRATEGY))
    if text != original:
        STRATEGY.write_text(text, encoding="utf-8")
        print("Guarded unsupported row layouts; aligned loaded-row offset")
    else:
        print("Step 015 already applied")


if __name__ == "__main__":
    main()
