#!/usr/bin/env python3
"""Retire tuple-row counting from visible-cargo sprite enumeration only."""

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

TARGET = Path("src/gestalt_graphics/gestalt_graphics.py")

OLD = """        # CABBAGE: output offsets still use legacy Road Hog row descriptors;
        # both NML and the compositor now derive them from GestaltGraphics.
        preceding_output_rows = 0
        row_groups = self.get_legacy_road_hog_output_row_groups(
            unit.model_variant.units
        )
        for preceding_unit, unit_row_groups in zip(unit.model_variant.units, row_groups):
            if preceding_unit is unit:
                break
            preceding_output_rows += sum(row_count for _, row_count in unit_row_groups)
        else:
            raise ValueError("Unit not found in model variant: " + unit.id)
"""

NEW = """        preceding_output_rows = 0
        for preceding_unit in unit.model_variant.units:
            if preceding_unit is unit:
                break
            preceding_output_rows += self.get_output_row_count_for_unit(
                preceding_unit
            )
        else:
            raise ValueError("Unit not found in model variant: " + unit.id)
"""

COUNT_METHOD = """    def get_output_row_count_for_unit(self, unit):
        # Count the rows emitted by the current Road Hog compositor, using
        # the same row types that drive its dispatch.
        if unit.always_use_same_spriterow:
            return 1
        result = 0
        for row_type in self.get_output_row_types():
            if row_type == "empty_vehicle_body":
                result += 1
            elif row_type == "bulk_cargo":
                result += 2 * len(polar_fox.constants.bulk_cargo_recolour_maps)
            elif row_type == "piece_cargo":
                result += 2 * len(
                    polar_fox.constants.piece_vehicle_type_to_sprites_maps[
                        self.piece_type
                    ]
                )
            elif row_type == "covered_vehicle_body":
                # CABBAGE: Road Hog compositor has no covered-body row handler.
                # Preserve the current non-emitting behaviour until implemented.
                continue
            else:
                raise ValueError(f"Unknown visible-cargo row type: {row_type}")
        return result

"""


def main():
    if not TARGET.is_file():
        raise SystemExit(f"Run from repository root: missing {TARGET}")
    original = TARGET.read_text(encoding="utf-8")
    tree = ast.parse(original)
    cls = next(
        (node for node in tree.body if isinstance(node, ast.ClassDef)
         and node.name == "GestaltGraphicsVisibleCargo"),
        None,
    )
    if cls is None:
        raise RuntimeError("Visible-cargo strategy missing")
    methods = {node.name: node for node in cls.body if isinstance(node, ast.FunctionDef)}
    if "get_unique_spritesets" not in methods:
        raise RuntimeError("Step 001 missing")
    source = original
    if OLD in source:
        if source.count(OLD) != 1:
            raise RuntimeError("Ambiguous offset calculation")
        source = source.replace(OLD, NEW, 1)
    elif NEW not in source:
        raise RuntimeError("Unexpected visible-cargo sprite offset calculation")
    if "get_output_row_count_for_unit" not in methods:
        anchor = "    def get_unique_spritesets(self, unit):"
        if source.count(anchor) != 1:
            raise RuntimeError("Ambiguous spriteset enumerator")
        source = source.replace(anchor, COUNT_METHOD + anchor, 1)
    elif COUNT_METHOD not in source:
        raise RuntimeError("Existing output-row counter differs from expected implementation")
    ast.parse(source, filename=str(TARGET))
    if source != original:
        TARGET.write_text(source, encoding="utf-8")
        print(f"Updated {TARGET}")
    print("Step 013: visible-cargo offsets no longer consume legacy tuple groups")


if __name__ == "__main__":
    main()
