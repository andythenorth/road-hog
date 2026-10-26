#!/usr/bin/env python3
"""Step 007: make Iron Horse visible-cargo row enumeration deterministic.

Cargo rows are numbered by cargo_row_map. Sorting the unique numeric row
indices preserves that physical row order instead of relying on set iteration.
No sprite geometry or compositor behaviour is changed in this step.
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
OLD = "        unique_cargo_rows = set(row_nums_seen)"
NEW = "        unique_cargo_rows = sorted(set(row_nums_seen))"


def main():
    if not TARGET.is_file():
        raise SystemExit("Run from the Road Hog repository root")
    source = TARGET.read_text(encoding="utf-8")
    tree = ast.parse(source)
    cls = next(
        (
            node
            for node in tree.body
            if isinstance(node, ast.ClassDef)
            and node.name == "GestaltGraphicsVisibleCargo"
        ),
        None,
    )
    if cls is None:
        raise RuntimeError("Missing GestaltGraphicsVisibleCargo")
    method = next(
        (
            node
            for node in cls.body
            if isinstance(node, ast.FunctionDef)
            and node.name == "get_unique_spritesets"
        ),
        None,
    )
    if method is None:
        raise RuntimeError("Step 001 must introduce get_unique_spritesets first")
    lines = source.splitlines(keepends=True)
    target_lines = lines[method.lineno - 1 : method.end_lineno]
    matching_old = [i for i, line in enumerate(target_lines) if line.rstrip("\n") == OLD]
    matching_new = [i for i, line in enumerate(target_lines) if line.rstrip("\n") == NEW]
    if not matching_old and len(matching_new) == 1:
        print("Step 007: already applied")
        return
    if len(matching_old) != 1 or matching_new:
        raise RuntimeError("Unexpected visible-cargo enumeration implementation")
    target_lines[matching_old[0]] = target_lines[matching_old[0]].replace(OLD, NEW, 1)
    lines[method.lineno - 1 : method.end_lineno] = target_lines
    result = "".join(lines)
    ast.parse(result)
    TARGET.write_text(result, encoding="utf-8")
    print("Step 007: cargo-row enumeration now uses numeric row order")


if __name__ == "__main__":
    main()
