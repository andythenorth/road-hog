#!/usr/bin/env python3
"""Add Iron Horse's unit spriteset naming interface to Road Hog.

This is an additive migration. Existing NML templates retain their callers.
Run from the Road Hog repository root.
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


TARGET = Path("src/road_vehicle/units.py")
METHOD_NAME = "get_spriteset_template_name"
METHOD = """    def get_spriteset_template_name(self, reversed, y):
        # Road Hog spriteset templates are named by unit ID, not train symmetry.
        # CABBAGE: migrate spriteset templates to the Iron Horse reusable symmetry-based approach.
        # The current road template does not distinguish reversed variants.
        return "spriteset_template_" + self.id + "(" + str(y) + ")"
"""


def main():
    if not TARGET.is_file():
        raise SystemExit(f"Run from repository root: missing {TARGET}")

    source = TARGET.read_text(encoding="utf-8")
    module = ast.parse(source)
    cls = next(
        (
            node
            for node in module.body
            if isinstance(node, ast.ClassDef) and node.name == "RoadVehicleUnit"
        ),
        None,
    )
    if cls is None:
        raise RuntimeError("RoadVehicleUnit class not found")

    if any(
        isinstance(node, ast.FunctionDef) and node.name == METHOD_NAME
        for node in cls.body
    ):
        note = "        # CABBAGE: migrate spriteset templates to the Iron Horse reusable symmetry-based approach."
        if note not in source:
            anchor = "        # Road Hog spriteset templates are named by unit ID, not train symmetry."
            if anchor not in source:
                raise RuntimeError("Existing method lacks expected comment anchor")
            source = source.replace(anchor, anchor + "\n" + note, 1)
            TARGET.write_text(source, encoding="utf-8")
            print(f"Added CABBAGE note: {TARGET}")
        else:
            print(f"Already migrated: {TARGET}")
        return

    if "def get_spriteset_template_name(" in source:
        raise RuntimeError("Unexpected existing spriteset method; refusing to modify")

    lines = source.splitlines(keepends=True)
    lines.insert(cls.end_lineno, "\n" + METHOD + "\n")
    result = "".join(lines)
    ast.parse(result)
    TARGET.write_text(result, encoding="utf-8")
    print(f"Added {METHOD_NAME} to {TARGET}")


if __name__ == "__main__":
    main()
