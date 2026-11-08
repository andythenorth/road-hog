#!/usr/bin/env python3
"""Correct naming migrations already applied; run from repository root."""
from pathlib import Path

changes = {
    Path("src/road_vehicle/schemas.py"): (
        "self.sprite_body_type =", "self.name_suffix_consist_type ="
    ),
    Path("src/road_vehicle/units.py"): (
        "self.model_variant.sprite_body_type.lower()",
        "self.model_variant.name_suffix_consist_type.lower()"
    ),
    Path("src/doc_helper.py"): (
        "translated_parts", "name_strings"
    ),
}
for path, (old, new) in changes.items():
    source = path.read_text()
    if old not in source:
        if new not in source:
            raise RuntimeError(f"{path}: neither expected form found")
        print(f"Already corrected: {path}")
        continue
    path.write_text(source.replace(old, new))
    print(f"Corrected: {path}")
