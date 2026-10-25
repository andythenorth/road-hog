#!/usr/bin/env python3
"""Default incomplete sprites for the current Road Hog fleet.

This is a genuine fleet default, not a declaration that any sprite is complete.
"""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODEL = ROOT / "src/road_vehicle/model_def.py"


def migrate(source):
    tree = ast.parse(source)
    classes = [n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "ModelDef"]
    if len(classes) != 1:
        raise RuntimeError("Expected exactly one ModelDef class")
    fields = [n for n in classes[0].body if isinstance(n, ast.AnnAssign)
              and isinstance(n.target, ast.Name) and n.target.id == "sprites_complete"]
    if len(fields) != 1:
        raise RuntimeError("Expected exactly one sprites_complete field")
    field = fields[0]
    if field.value is not None:
        if isinstance(field.value, ast.Constant) and field.value.value is False:
            return source
        raise RuntimeError("sprites_complete already has a different default")
    if not isinstance(field.annotation, ast.Name) or field.annotation.id != "bool":
        raise RuntimeError("Unexpected sprites_complete type")
    # Only replace the field's own line; keep surrounding comments and formatting.
    lines = source.splitlines(keepends=True)
    line = lines[field.lineno - 1]
    if line.strip() != "sprites_complete: bool":
        raise RuntimeError("Unexpected sprites_complete declaration format")
    indent = line[:len(line) - len(line.lstrip())]
    ending = "\r\n" if line.endswith("\r\n") else "\n"
    lines[field.lineno - 1] = (
        indent + "# CABBAGE: All existing Road Hog vehicles have incomplete sprites."
        + ending + indent + "sprites_complete: bool = False" + ending
    )
    updated = "".join(lines)
    ast.parse(updated)
    return updated


def main():
    previous = MODEL.read_text(encoding="utf-8")
    updated = migrate(previous)
    if updated != previous:
        MODEL.write_text(updated, encoding="utf-8")
        print("UPDATED: src/road_vehicle/model_def.py")
    else:
        print("UNCHANGED: src/road_vehicle/model_def.py")
    print("PASS: sprites_complete defaults to False; explicit True/False preserved")


if __name__ == "__main__":
    main()
