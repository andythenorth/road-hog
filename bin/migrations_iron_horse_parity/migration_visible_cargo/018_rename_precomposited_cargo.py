#!/usr/bin/env python3
"""Rename Road Hog visible-cargo strategy and template to Iron Horse names.

This is naming convergence only; existing rendering semantics are preserved.
"""

import ast
from pathlib import Path

OLD_CLASS = "GestaltGraphicsVisibleCargo"
NEW_CLASS = "GestaltGraphicsPrecompositedCargo"
OLD_TEMPLATE = "vehicle_with_visible_cargo.pynml"
NEW_TEMPLATE = "vehicle_with_precomposited_cargo.pynml"
SRC = Path("src")
TEMPLATES = SRC / "templates"


def main():
    strategy_path = SRC / "gestalt_graphics" / "gestalt_graphics.py"
    original_template = TEMPLATES / OLD_TEMPLATE
    renamed_template = TEMPLATES / NEW_TEMPLATE
    if not strategy_path.is_file() or not TEMPLATES.is_dir():
        raise RuntimeError("Run from the Road Hog repository root")

    candidates = sorted(SRC.rglob("*.py")) + sorted(SRC.rglob("*.pynml"))
    updates = {}
    for path in candidates:
        original = path.read_text(encoding="utf-8")
        revised = original.replace(OLD_CLASS, NEW_CLASS).replace(
            OLD_TEMPLATE, NEW_TEMPLATE
        )
        if revised != original:
            if path.suffix == ".py":
                ast.parse(revised, filename=str(path))
            updates[path] = revised

    if original_template.exists() and renamed_template.exists():
        raise RuntimeError("Both old and new templates exist: refusing ambiguous rename")
    if not original_template.exists() and not renamed_template.exists():
        raise RuntimeError("Neither old nor new visible-cargo template exists")

    strategy = updates.get(strategy_path, strategy_path.read_text(encoding="utf-8"))
    tree = ast.parse(strategy)
    classes = {
        node.name for node in tree.body if isinstance(node, ast.ClassDef)
    }
    if NEW_CLASS not in classes or OLD_CLASS in classes:
        raise RuntimeError("Expected exactly the renamed gestalt class")

    if not original_template.exists() and updates:
        raise RuntimeError("Partially renamed source detected; refusing further changes")
    if not updates and not original_template.exists():
        print("Step 018: already renamed; no changes")
        return

    # Validate all proposed edits before writing any source file.
    for path, revised in updates.items():
        path.write_text(revised, encoding="utf-8")
    if original_template.exists():
        original_template.rename(renamed_template)
    print(f"Step 018: renamed {OLD_CLASS} and {OLD_TEMPLATE}")


if __name__ == "__main__":
    main()
