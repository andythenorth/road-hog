"""Remove unused legacy road_vehicle imports from src/vehicles modules.

Run from the repository root.  This deliberately limits changes to simple,
single-line ``from road_vehicle import ...`` statements; it does not rewrite
vehicle definitions or imports from other packages.
"""

import ast
from pathlib import Path


VEHICLES = Path("src/vehicles")


def clean_module(path):
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    loaded_names = {
        node.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
    }
    lines = source.splitlines(keepends=True)
    removed = 0

    for node in ast.walk(tree):
        if not isinstance(node, ast.ImportFrom) or node.module != "road_vehicle":
            continue
        if node.level or node.lineno != node.end_lineno:
            raise ValueError(f"Unsupported multiline import at {path}:{node.lineno}")
        if any(alias.name == "*" for alias in node.names):
            continue

        retained = [
            alias
            for alias in node.names
            if (alias.asname or alias.name) in loaded_names
        ]
        removed += len(node.names) - len(retained)
        if len(retained) == len(node.names):
            continue

        index = node.lineno - 1
        old_line = lines[index]
        if "#" in old_line or ";" in old_line:
            raise ValueError(f"Import needs manual review: {path}:{node.lineno}")
        if not old_line.lstrip().startswith("from road_vehicle import "):
            raise ValueError(f"Unexpected import format: {path}:{node.lineno}")
        if retained:
            indent = old_line[: len(old_line) - len(old_line.lstrip())]
            names = ", ".join(
                alias.name + (f" as {alias.asname}" if alias.asname else "")
                for alias in retained
            )
            newline = "\r\n" if old_line.endswith("\r\n") else "\n"
            lines[index] = f"{indent}from road_vehicle import {names}{newline}"
        else:
            lines[index] = ""

    if removed:
        updated = "".join(lines)
        ast.parse(updated, filename=str(path))
        path.write_text(updated, encoding="utf-8")
    return removed


def main():
    if not VEHICLES.is_dir():
        raise SystemExit("Run from Road Hog repository root: src/vehicles missing")
    files_changed = 0
    imports_removed = 0
    for path in sorted(VEHICLES.glob("*.py")):
        count = clean_module(path)
        if count:
            print(f"{path}: removed {count} unused import(s)")
            files_changed += 1
            imports_removed += count
    print(f"Changed {files_changed} files; removed {imports_removed} imports")


if __name__ == "__main__":
    main()
