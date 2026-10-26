#!/usr/bin/env python3
"""Standalone additive migration of Iron Horse visible-cargo row interfaces.

Run from Road Hog repository root. No existing rendering callers are changed.
"""

from pathlib import Path
import ast
import sys

TARGET = Path("src/gestalt_graphics/gestalt_graphics.py")
CLASS_NAME = "GestaltGraphicsVisibleCargo"
METHODS = {'get_output_row_types': '    def get_output_row_types(self):\n        # note that this is *types* of rows, in order, not counts - counts are delegated elsehwere\n        result = []\n        # for e.g. tarpaulin cars, covered coil cars, insert a specific spriterow to show the cover when 100% loaded or travelling\n        if self.covered_vehicle_body:\n            result.append("covered_vehicle_body")\n        # 1 empty spriterow\n        result.append("empty_vehicle_body")\n        if self.has_bulk:\n            result.append("bulk_cargo")\n        if self.has_piece:\n            result.append("piece_cargo")\n        return result', 'get_unique_spritesets': '    def get_unique_spritesets(self, unit):\n        # the template for this gestalt was getting complex with loops and logic where logic shouldn\'t be\n        # so instead we delegate that logic here and simplify the loop\n        # this builds heavily on the row numbers already in cargo_row_map, reformatting that data to make it easy to render in the template\n        row_nums_seen = []\n        result = []\n        for row_nums in self.cargo_row_map.values():\n            for row_num in row_nums:\n                row_nums_seen.append(row_num)\n        unique_cargo_rows = set(row_nums_seen)\n\n        row_height = graphics_constants.spriterow_height\n\n        start_y_cumulative = graphics_constants.spritesheet_top_margin\n\n        if self.covered_vehicle_body:\n            # add rows for covered sprite\n            for weathered_state in self.weathered_states.keys():\n                result.append(["has_cover_" + weathered_state, start_y_cumulative])\n                start_y_cumulative += row_height\n\n        # add rows for empty sprite\n        for weathered_state in self.weathered_states.keys():\n            result.append(["empty_" + weathered_state, start_y_cumulative])\n            start_y_cumulative += row_height\n\n        # !! not sure unique_cargo_rows order will always reliably match to what\'s needed, but if it doesn\'t, explicitly sort it eh\n        for row_num in unique_cargo_rows:\n            result.append(\n                [\n                    "loading_" + str(row_num),\n                    start_y_cumulative,\n                ]\n            )\n            result.append(\n                [\n                    "loaded_" + str(row_num),\n                    start_y_cumulative + 30,\n                ]\n            )\n            start_y_cumulative += 2 * row_height\n\n        # vehicles with multiple units might need an offset to their sprites\n        # to handle that we post-process the y-offsets in result\n        # we make an assumption that the spriterows will always be vertically contiguous\n        # so we can take the last value of start_y_cumulative, apply the offset multiplier, then rewrite the y values in result\n        # n.b. by default force_spriterow_group_in_output_spritesheet = 0, so this has no effect unless explicitly set\n        vehicle_y_offset = unit.unit_def.force_spriterow_group_in_output_spritesheet * (\n            start_y_cumulative - graphics_constants.spritesheet_top_margin\n        )\n        for row_map in result:\n            row_map[1] = row_map[1] + vehicle_y_offset\n        return result'}
STATE = '        # State needed by the copied Iron Horse row-enumeration methods.\n        self.covered_vehicle_body = kwargs.get("covered_vehicle_body", False)\n        self.weathered_states = kwargs.get(\n            "weathered_states", {"unweathered": self.body_recolour_map}\n        )\n'


def locate_class(source):
    module = ast.parse(source)
    cls = next(
        (node for node in module.body if isinstance(node, ast.ClassDef) and node.name == CLASS_NAME),
        None,
    )
    if cls is None:
        raise RuntimeError(f"Missing {CLASS_NAME} in {TARGET}")
    return cls


def main():
    if not TARGET.is_file():
        raise SystemExit(f"Run from the repository root: missing {TARGET}")
    source = TARGET.read_text(encoding="utf-8")
    cls = locate_class(source)
    present = {node.name for node in cls.body if isinstance(node, ast.FunctionDef)}
    if any(name in present for name in METHODS) and not all(
        name in present for name in METHODS
    ):
        raise RuntimeError("Partial Iron Horse method migration; refusing to overwrite")
    if all(name in present for name in METHODS):
        print("Already migrated; no changes")
        return
    if "self.weathered_states" in source or "self.covered_vehicle_body" in source:
        raise RuntimeError("Existing weather/cover state requires manual review")
    # Insert compatible state only in the target class constructor.
    ctor = next(
        (node for node in cls.body if isinstance(node, ast.FunctionDef) and node.name == "__init__"),
        None,
    )
    if ctor is None:
        raise RuntimeError("Missing visible-cargo constructor")
    lines = source.splitlines(keepends=True)
    # Copy Iron Horse methods unchanged; they are not used until later migration steps.
    insert_at = cls.end_lineno
    lines.insert(insert_at, "\n" + "\n\n".join(METHODS.values()) + "\n")
    source = "".join(lines)
    cls = locate_class(source)
    ctor = next(node for node in cls.body if isinstance(node, ast.FunctionDef) and node.name == "__init__")
    lines = source.splitlines(keepends=True)
    # Constructor state defaults support the newly copied methods without altering pipelines.
    lines.insert(ctor.end_lineno, STATE)
    result = "".join(lines)
    ast.parse(result)
    TARGET.write_text(result, encoding="utf-8")
    print(f"Updated {TARGET}: {', '.join(METHODS)}")


if __name__ == "__main__":
    main()
