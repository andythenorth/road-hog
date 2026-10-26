#!/usr/bin/env python3
"""Converge compositor margin usage and fail explicitly for unknown row types."""

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

PIPELINE = Path("src/gestalt_graphics/pipelines.py")


def main():
    if not PIPELINE.is_file():
        raise SystemExit(f"Run from repository root: missing {PIPELINE}")
    original = PIPELINE.read_text(encoding="utf-8")
    text = original
    old = """                elif spriterow_type == "piece_cargo":
                    source_spriterow_count = 2
                    self.add_piece_cargo_spriterows()
                consist_cumulative_source_spriterow_count += source_spriterow_count
"""
    new = """                elif spriterow_type == "piece_cargo":
                    source_spriterow_count = 2
                    self.add_piece_cargo_spriterows()
                else:
                    raise ValueError(f"Unsupported compositor row type: {spriterow_type}")
                consist_cumulative_source_spriterow_count += source_spriterow_count
"""
    if old in text:
        if text.count(old) != 1:
            raise RuntimeError("Unexpected compositor row dispatch count")
        text = text.replace(old, new, 1)
    elif new not in text:
        raise RuntimeError("Unrecognised compositor row dispatch")

    old_base = """            vehicle_unit_source_base_yoffs = 10 + (
                graphics_constants.spriterow_height
                * consist_cumulative_source_spriterow_count
            )
"""
    new_base = """            vehicle_unit_source_base_yoffs = graphics_constants.spritesheet_top_margin + (
                graphics_constants.spriterow_height
                * consist_cumulative_source_spriterow_count
            )
"""
    if old_base in text:
        text = text.replace(old_base, new_base, 1)
    elif new_base not in text:
        raise RuntimeError("Unrecognised compositor source base offset")

    ast.parse(text, filename=str(PIPELINE))
    if text != original:
        PIPELINE.write_text(text, encoding="utf-8")
        print("Step 016: explicit row dispatch failure and shared margin constant")
    else:
        print("Step 016 already applied")


if __name__ == "__main__":
    main()
