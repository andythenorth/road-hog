#!/usr/bin/env python3
"""Migrate active Road Hog single-unit vehicles into the non-articulated ID range.

Run at the repository root:
    python bin/mig014_vehicle_ids/014_migrate_vehicle_ids.py

All existing articulated IDs are preserved. The migration edits only the integer
literal of base_numeric_id in active single-unit vehicle declarations.
"""

import argparse
import ast
from collections import defaultdict
from pathlib import Path
import re

MAX_ARTICULATED_ID = 16383
FIRST_SINGLE_UNIT_ID = 16400
BLOCK_SIZE = 10
ROSTERS = ("landrace", "heqs")


def literal_int(node, context):
    if not isinstance(node, ast.Constant) or type(node.value) is not int:
        raise RuntimeError(f"Expected literal integer for {context} (line {node.lineno})")
    return node.value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Show proposed changes without writing")
    args = parser.parse_args()

    root = Path.cwd()
    vehicles_dir = root / "src" / "vehicles"
    if not vehicles_dir.is_dir():
        raise SystemExit("Run from the Road Hog repository root (src/vehicles missing)")

    # Read only the vehicle modules actually registered by the rosters.
    modules = set()
    for roster_name in ROSTERS:
        filename = root / "src" / "rosters" / f"{roster_name}.py"
        tree = ast.parse(filename.read_text(), filename=str(filename))
        roster_calls = [
            node for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            and node.func.id == "Roster"
        ]
        if len(roster_calls) != 1:
            raise RuntimeError(f"Expected exactly one Roster(...) in {filename}")
        roster_call = roster_calls[0]
        vehicles_arg = next((kw.value for kw in roster_call.keywords if kw.arg == "vehicles"), None)
        if not isinstance(vehicles_arg, (ast.List, ast.Tuple)):
            raise RuntimeError(f"Expected literal vehicles list in {filename}")
        for element in vehicles_arg.elts:
            if not isinstance(element, ast.Name):
                raise RuntimeError(f"Unexpected vehicle registration in {filename}:{element.lineno}")
            modules.add(element.id)

    declared = []
    for module in sorted(modules):
        filename = vehicles_dir / f"{module}.py"
        source = filename.read_text()
        tree = ast.parse(source, filename=str(filename))
        model_calls = [
            node for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            and node.func.id == "ModelDef"
        ]
        if len(model_calls) != 1:
            raise RuntimeError(f"Expected exactly one ModelDef(...) in {filename}")
        call = model_calls[0]
        numeric_kw = next((kw for kw in call.keywords if kw.arg == "base_numeric_id"), None)
        if numeric_kw is None:
            raise RuntimeError(f"Missing base_numeric_id in {filename}")
        base_id = literal_int(numeric_kw.value, f"{filename}:base_numeric_id")
        if base_id % BLOCK_SIZE:
            raise RuntimeError(f"Non-block-aligned existing ID: {module}={base_id}")

        unit_calls = [
            node for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
            and node.func.attr == "add_unit_def"
        ]
        if not unit_calls:
            raise RuntimeError(f"No add_unit_def calls found in {filename}")
        actual_units = 0
        for unit_call in unit_calls:
            repeat_kw = next((kw for kw in unit_call.keywords if kw.arg == "repeat"), None)
            repeat = literal_int(repeat_kw.value, f"{filename}:repeat") if repeat_kw else 1
            if repeat < 1:
                raise RuntimeError(f"Invalid unit repeat in {filename}")
            actual_units += repeat
        declared.append((base_id, module, filename, source, numeric_kw.value, actual_units, len(unit_calls)))

    # Check existing block allocation, including dormant candidates being untouched.
    by_base = defaultdict(list)
    for base, module, *_ in declared:
        by_base[base].append(module)
    overlaps = {base: names for base, names in by_base.items() if len(names) > 1}
    if overlaps:
        raise RuntimeError(f"Duplicate active base ID blocks: {overlaps}")

    singles = sorted((item for item in declared if item[5] == 1), key=lambda item: (item[0], item[1]))
    articulated = [item for item in declared if item[5] > 1]
    for base, module, *_ in articulated:
        if base > MAX_ARTICULATED_ID:
            raise RuntimeError(f"Articulated vehicle {module} already outside allocated ID range: {base}")
    occupied = {base for base, module, *_ in declared if base > MAX_ARTICULATED_ID and module not in {s[1] for s in singles}}
    target_ids = []
    candidate = FIRST_SINGLE_UNIT_ID
    for _ in singles:
        while candidate in occupied:
            candidate += BLOCK_SIZE
        if candidate > 65530:
            raise RuntimeError("Exhausted vehicle ID range")
        target_ids.append(candidate)
        occupied.add(candidate)
        candidate += BLOCK_SIZE

    changes = []
    for item, new_id in zip(singles, target_ids):
        old_id, module, filename, source, value_node, _, unit_defs = item
        if old_id == new_id:
            continue
        lines = source.splitlines(keepends=True)
        if value_node.lineno != value_node.end_lineno:
            raise RuntimeError(f"Unexpected multiline base ID in {filename}")
        line_index = value_node.lineno - 1
        line = lines[line_index]
        start, end = value_node.col_offset, value_node.end_col_offset
        if line[start:end] != str(old_id):
            raise RuntimeError(f"Could not identify exact base_numeric_id literal in {filename}")
        lines[line_index] = line[:start] + str(new_id) + line[end:]
        updated = "".join(lines)
        ast.parse(updated, filename=str(filename))
        changes.append((module, old_id, new_id, filename, updated))

    for module, old_id, new_id, *_ in changes:
        print(f"{module}: {old_id} -> {new_id}")
    print(f"{len(changes)} single-unit vehicle IDs {'would be' if args.check else 'were'} migrated; "
          f"{len(articulated)} articulated base IDs unchanged")
    if not args.check:
        for _, _, _, filename, updated in changes:
            filename.write_text(updated)


if __name__ == "__main__":
    main()
