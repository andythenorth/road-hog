#!/usr/bin/env python3
"""Migrate visible-cargo cargo_row_map to the Iron Horse implementation."""

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
CLASS_NAME = "GestaltGraphicsVisibleCargo"

# Adapted from Iron Horse GestaltGraphicsPrecompositedCargo.cargo_row_map.
# Retain @property because Road Hog does not currently cache this mapping.
IRON_HORSE_CARGO_ROW_MAP = """    @property
    def cargo_row_map(self):
        result = {}
        counter = 0
        if self.has_bulk:
            for cargo_map in polar_fox.constants.bulk_cargo_recolour_maps:
                result[cargo_map[0]] = [counter]
                counter += 1
        if self.has_piece:
            for cargo_filename in polar_fox.constants.piece_vehicle_type_to_sprites_maps[
                self.piece_type
            ]:
                for cargo_label in polar_fox.constants.piece_sprites_to_cargo_labels_maps[
                    cargo_filename
                ]:
                    result.setdefault(cargo_label, []).append(counter)
                counter += 1
        return result
"""

LEGACY_COMMENT = (
    "        # CABBAGE: legacy piece_cargo_maps is still required by the Road Hog "
    "compositor; retire when its caller migrates.\n"
)


def get_class(tree):
    return next(
        (
            node
            for node in tree.body
            if isinstance(node, ast.ClassDef) and node.name == CLASS_NAME
        ),
        None,
    )


def get_method(cls, name):
    return next(
        (
            node
            for node in cls.body
            if isinstance(node, ast.FunctionDef) and node.name == name
        ),
        None,
    )


def main():
    if not TARGET.is_file():
        raise SystemExit(f"Run from repository root: missing {TARGET}")

    original = TARGET.read_text(encoding="utf-8")
    source = original
    tree = ast.parse(source)
    cls = get_class(tree)
    if cls is None:
        raise RuntimeError(f"Missing {CLASS_NAME}")

    method = get_method(cls, "cargo_row_map")
    legacy = get_method(cls, "piece_cargo_maps")
    if method is None:
        raise RuntimeError("Unexpected visible-cargo mapping; refusing to patch")
    if legacy is None:
        method_text = ast.get_source_segment(source, method)
        if method_text and "piece_vehicle_type_to_sprites_maps" in method_text:
            print("Already migrated: legacy piece-cargo property retired")
            return
        raise RuntimeError("Legacy property absent but mapping is not migrated")

    method_text = ast.get_source_segment(source, method)
    if method_text is None:
        raise RuntimeError("Unable to identify cargo_row_map")
    if "piece_cargo_maps" not in method_text:
        if "piece_vehicle_type_to_sprites_maps" in method_text:
            if LEGACY_COMMENT in source:
                print("Already migrated: cargo_row_map")
                return
            raise RuntimeError("Cargo mapping migrated but legacy boundary unmarked")
        raise RuntimeError("Unexpected cargo mapping implementation")

    # Replace the decorated property as one region, preserving surrounding methods.
    start = min([method.lineno] + [node.lineno for node in method.decorator_list])
    stop = method.end_lineno
    lines = source.splitlines(keepends=True)
    lines[start - 1 : stop] = [IRON_HORSE_CARGO_ROW_MAP + "\n"]
    source = "".join(lines)

    tree = ast.parse(source)
    cls = get_class(tree)
    legacy = get_method(cls, "piece_cargo_maps")
    if legacy is None:
        raise RuntimeError("Lost legacy compositor interface")
    lines = source.splitlines(keepends=True)
    # Insert inside legacy property as explicit temporary-compatibility marker.
    lines.insert(legacy.body[0].lineno - 1, LEGACY_COMMENT)
    result = "".join(lines)
    ast.parse(result)
    TARGET.write_text(result, encoding="utf-8")
    print(f"Migrated cargo-row mapping: {TARGET}")


if __name__ == "__main__":
    main()
