#!/usr/bin/env python3
"""Align visible-cargo NML row offsets with the existing Road Hog compositor.

Use the compositor's per-unit output-row counts, including its one-row
fixed-body case. Do not change the physical spritesheet or template selection.
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

TARGET = Path("src/gestalt_graphics/gestalt_graphics.py")
OLD = '''        for row_map in result:
            row_map[1] = row_map[1] + vehicle_y_offset
        return result'''
NEW = '''        # CABBAGE: output grouping still follows the legacy Road Hog compositor;
        # migrate it to Iron Horse's row-type contract with the pipeline.
        preceding_output_rows = 0
        for preceding_unit in unit.model_variant.units:
            if preceding_unit is unit:
                break
            if preceding_unit.always_use_same_spriterow:
                preceding_output_rows += 1
            else:
                preceding_output_rows += sum(
                    row_count
                    for _, row_count in self.get_output_row_counts_by_type()
                )
        else:
            raise ValueError("Unit not found in model variant: " + unit.id)

        preceding_y_offset = preceding_output_rows * row_height
        if unit.always_use_same_spriterow:
            # The compositor emits one row for this unit, but the existing NML
            # switches still need empty/loading/loaded spriteset names.
            fixed_y = (
                graphics_constants.spritesheet_top_margin + preceding_y_offset
            )
            for row_map in result:
                row_map[1] = fixed_y
        else:
            for row_map in result:
                row_map[1] += preceding_y_offset + vehicle_y_offset
        return result'''


def main():
    if not TARGET.is_file():
        raise SystemExit("Run from the Road Hog repository root")
    source = TARGET.read_text(encoding="utf-8")
    tree = ast.parse(source)
    strategy = next(
        (
            node
            for node in tree.body
            if isinstance(node, ast.ClassDef)
            and node.name == "GestaltGraphicsVisibleCargo"
        ),
        None,
    )
    if strategy is None:
        raise RuntimeError("Missing GestaltGraphicsVisibleCargo")
    method = next(
        (
            node
            for node in strategy.body
            if isinstance(node, ast.FunctionDef)
            and node.name == "get_unique_spritesets"
        ),
        None,
    )
    if method is None:
        raise RuntimeError("Step 001 must run first")
    lines = source.splitlines(keepends=True)
    start = method.lineno - 1
    end = method.end_lineno
    method_source = "".join(lines[start:end])
    # Steps 009 and 013 supersede this offset implementation.  Recognise their
    # complete calculation, not just an identifier, before declaring success.
    successor_calculation = (
        "preceding_output_rows += self.get_output_row_count_for_unit("
        in method_source
        and "preceding_y_offset = preceding_output_rows * row_height"
        in method_source
        and "row_map[1] += preceding_y_offset + vehicle_y_offset"
        in method_source
    )
    legacy_step_009_calculation = (
        "get_legacy_road_hog_output_row_groups(" in method_source
        and "preceding_y_offset = preceding_output_rows * row_height"
        in method_source
    )
    if (successor_calculation or legacy_step_009_calculation) and OLD not in method_source:
        print("Step 008: superseded by a later row-offset implementation")
        return
    if NEW in method_source and OLD not in method_source:
        print("Step 008: already applied")
        return
    if method_source.count(OLD) != 1 or NEW in method_source:
        raise RuntimeError("Unexpected enumerator layout; refusing to change it")
    lines[start:end] = [method_source.replace(OLD, NEW, 1)]
    updated = "".join(lines)
    ast.parse(updated)
    TARGET.write_text(updated, encoding="utf-8")
    print("Step 008: articulated output row offsets aligned")


if __name__ == "__main__":
    main()
