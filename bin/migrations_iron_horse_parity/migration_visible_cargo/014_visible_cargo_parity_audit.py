#!/usr/bin/env python3
"""Audit visible-cargo migration boundaries without altering rendering semantics."""

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

OBSOLETE_COMMENT = (
    "        # !! not sure unique_cargo_rows order will always reliably match to "
    "what's needed, but if it doesn't, explicitly sort it eh\n"
)


def class_methods(path, name):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    cls = next(
        (node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == name),
        None,
    )
    if cls is None:
        raise RuntimeError(f"Missing {name} in {path}")
    return {node.name for node in cls.body if isinstance(node, ast.FunctionDef)}


def main():
    for path in (STRATEGY, PIPELINE, TEMPLATE):
        if not path.is_file():
            raise SystemExit(f"Run from repository root: missing {path}")

    strategy = STRATEGY.read_text(encoding="utf-8")
    if OBSOLETE_COMMENT in strategy:
        strategy = strategy.replace(OBSOLETE_COMMENT, "", 1)
        ast.parse(strategy, filename=str(STRATEGY))
        STRATEGY.write_text(strategy, encoding="utf-8")
        print("Removed obsolete cargo-row ordering comment")

    methods = class_methods(STRATEGY, "GestaltGraphicsVisibleCargo")
    required = {
        "get_unique_spritesets",
        "get_output_row_types",
        "get_spriterow_types_for_units",
        "get_output_row_count_for_unit",
    }
    missing = required - methods
    if missing:
        raise RuntimeError(f"Missing visible-cargo interfaces: {sorted(missing)}")
    if "unique_cargo_rows = sorted(set(row_nums_seen))" not in strategy:
        raise RuntimeError("Cargo-row enumeration is not deterministic")
    if "preceding_output_rows += self.get_output_row_count_for_unit(" not in strategy:
        raise RuntimeError("Articulated offsets do not use output row counts")

    pipeline = PIPELINE.read_text(encoding="utf-8")
    if "get_spriterow_types_for_units(" not in pipeline:
        raise RuntimeError("Compositor does not consume strategy row types")
    template = TEMPLATE.read_text(encoding="utf-8")
    if "get_unique_spritesets(" not in template:
        raise RuntimeError("NML template does not enumerate strategy spritesets")
    if "get_spriteset_template_name(" not in template:
        raise RuntimeError("NML template does not use unit spriteset interface")

    print("Visible-cargo interface and caller checks: PASS")
    print("Deferred boundaries (not removed by this pass):")
    print("- Shared get_output_row_counts_by_type and legacy row grouping: used by other strategies")
    print("- Road Hog fixed-row articulated handling: explicit CABBAGE compatibility")
    print("- Road Hog cargo composition geometry and purchase sprites: not Iron Horse parity")
    print("- Unit-specific spriteset template naming: future separate migration")
    print("Full make and GRF production: must be verified in repository")


if __name__ == "__main__":
    main()
