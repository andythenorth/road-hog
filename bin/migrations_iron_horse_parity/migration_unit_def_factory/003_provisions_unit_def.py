#!/usr/bin/env python3
"""Move concrete UnitDef configuration from Unit constructors to ModelVariantProducer.

Run from the Road Hog repository root, against the pre-002 source.
"""

import ast
import json
from pathlib import Path


ROOT = Path.cwd()
CATALOGUE = ROOT / "src/road_vehicle/catalogue.py"
UNITS = ROOT / "src/road_vehicle/units.py"


def replace_once(source, old, new, path):
    if source.count(old) != 1:
        raise ValueError(f"Expected one occurrence in {path}: {old[:70]!r}")
    return source.replace(old, new, 1)


def patch_catalogue(source):
    source = replace_once(
        source,
        "from dataclasses import dataclass",
        "from dataclasses import dataclass, fields, replace\n\nfrom .model_def import UnitDef",
        CATALOGUE,
    )
    source = replace_once(
        source,
        "            unit_cls = getattr(units, unit_def.unit_cls_name)\n"
        "            unit = unit_cls(\n"
        "                model_variant=model_variant,\n"
        "                unit_def=unit_def,",
        "            unit_cls = getattr(units, unit_def.unit_cls_name)\n"
        "            if unit_cls.provisions_unit_def:\n"
        "                unit_def = replace(\n"
        "                    unit_def,\n"
        "                    **{\n"
        "                        field.name: getattr(unit_cls, f\"_{field.name}\")\n"
        "                        for field in fields(UnitDef)\n"
        "                        if field.name not in (\"unit_cls_name\", \"repeat\")\n"
        "                        and hasattr(unit_cls, f\"_{field.name}\")\n"
        "                    },\n"
        "                )\n"
        "            unit = unit_cls(\n"
        "                model_variant=model_variant,\n"
        "                unit_def=unit_def,",
        CATALOGUE,
    )
    return source


def patch_units(source):
    source = replace_once(
        source,
        "class RoadVehicleUnit:\n",
        "class RoadVehicleUnit:\n    provisions_unit_def = False\n\n",
        UNITS,
    )
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    changes = []
    converted = []

    for cls in tree.body:
        if not isinstance(cls, ast.ClassDef):
            continue
        for method in cls.body:
            if not isinstance(method, ast.FunctionDef) or method.name != "__init__":
                continue
            calls = [
                call
                for call in ast.walk(method)
                if isinstance(call, ast.Call)
                and isinstance(call.func, ast.Name)
                and call.func.id == "replace"
            ]
            if not calls:
                continue
            if len(calls) != 1 or len(method.body) != 3:
                raise ValueError(f"Unexpected constructor in {cls.name}")
            props = [
                (kw.arg, ast.literal_eval(kw.value)) for kw in calls[0].keywords
            ]
            if any(name is None for name, _ in props):
                raise ValueError(f"Unexpected **kwargs in {cls.name}")

            body = "    provisions_unit_def = True\n"
            for name, value in props:
                if isinstance(value, list):
                    expr = "[" + ", ".join(json.dumps(item) for item in value) + "]"
                    if len(f"    _{name} = {expr}") > 88:
                        body += f"    _{name} = [\n"
                        for item in value:
                            body += f"        {json.dumps(item)},\n"
                        body += "    ]\n"
                        continue
                elif isinstance(value, str):
                    expr = json.dumps(value)
                else:
                    expr = repr(value)
                body += f"    _{name} = {expr}\n"

            changes.append((method.lineno - 1, method.end_lineno, body))
            converted.append(cls.name)

    if len(converted) != 25:
        raise ValueError(f"Expected 25 concrete constructors, found {len(converted)}")
    for start, end, body in sorted(changes, reverse=True):
        lines[start:end] = [body]
    return "".join(lines), converted


def main():
    catalogue = CATALOGUE.read_text()
    units = UNITS.read_text()
    new_catalogue = patch_catalogue(catalogue)
    new_units, converted = patch_units(units)
    ast.parse(new_catalogue)
    ast.parse(new_units)
    CATALOGUE.write_text(new_catalogue)
    UNITS.write_text(new_units)
    print(f"PASS: converted {len(converted)} Units; changed catalogue.py and units.py")


if __name__ == "__main__":
    main()
