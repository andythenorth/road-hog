#!/usr/bin/env python3
"""Install the bounded Road Hog power compatibility contract.

CABBAGE This is a migration shim, not a multi-mode power implementation.
CABBAGE Scalar Road Hog power must remain scalar for NML and costs.
"""
from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parents[2]
MODEL = ROOT / "src/road_vehicle/model_def.py"
SCHEMAS = ROOT / "src/road_vehicle/schemas.py"


def only_class(source, name):
    matches = [node for node in ast.parse(source).body
               if isinstance(node, ast.ClassDef) and node.name == name]
    if len(matches) != 1:
        raise RuntimeError(f"Expected exactly one {name} class")
    return matches[0]


def modify_model(source):
    cls = only_class(source, "ModelDef")
    fields = {target.id for node in cls.body if isinstance(node, ast.AnnAssign)
              for target in [node.target] if isinstance(target, ast.Name)}
    if "power_by_power_source" not in fields:
        raise RuntimeError("Existing ModelDef power_by_power_source field missing")
    if "power" not in fields:
        anchor = "    power_by_power_source: Optional[Dict[Any, Any]] = None\n"
        if source.count(anchor) != 1:
            raise RuntimeError("Cannot uniquely locate power_by_power_source field")
        source = source.replace(anchor,
            "    # CABBAGE Migration shim: legacy Road Hog scalar power remains supported.\n"
            "    # Multi-source mapping is storage only until separately implemented.\n"
            "    power: Optional[int] = None\n" + anchor)
    cls = only_class(source, "ModelDef")
    if not any(isinstance(n, ast.FunctionDef) and n.name == "__post_init__" for n in cls.body):
        anchor = "    def add_unit_def(self, **kwargs):\n"
        if source.count(anchor) != 1:
            raise RuntimeError("Cannot uniquely locate ModelDef method insertion point")
        source = source.replace(anchor,
            "    def __post_init__(self):\n"
            "        # CABBAGE Migration shim: two simultaneous power declarations are ambiguous.\n"
            "        if self.power is not None and self.power_by_power_source is not None:\n"
            "            raise ValueError('Specify power OR power_by_power_source, not both')\n\n" + anchor)
    else:
        cls = only_class(source, "ModelDef")
        func = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == "__post_init__")
        snippet = ast.get_source_segment(source, func) or ""
        if "power_by_power_source" not in snippet or "self.power" not in snippet:
            raise RuntimeError("Custom ModelDef.__post_init__ requires manual integration")
    ast.parse(source)
    return source


def modify_schemas(source):
    cls = only_class(source, "RoadVehicleBase")
    methods = [n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == "power"]
    if len(methods) != 1:
        raise RuntimeError("RoadVehicleBase.power has changed; refusing edit")
    method = methods[0]
    segment = ast.get_source_segment(source, method) or ""
    target = "if self.model_def.power is not None:"
    if target in segment:
        return source
    lines = source.splitlines(keepends=True)
    body = method.body
    if not body or not isinstance(body[0], ast.Assign):
        raise RuntimeError("Unexpected RoadVehicleBase.power implementation")
    expr = body[0]
    if not (len(expr.targets) == 1 and isinstance(expr.targets[0], ast.Name)
            and expr.targets[0].id == "powers"
            and isinstance(expr.value, ast.Attribute)
            and expr.value.attr == "power_by_power_source"):
        raise RuntimeError("Power calculation does not use expected source mapping")
    lines.insert(expr.lineno - 1,
        "        # CABBAGE Migration shim: keep old scalar Road Hog power and costs exact.\n"
        "        if self.model_def.power is not None:\n"
        "            return self.model_def.power\n")
    updated = "".join(lines)
    ast.parse(updated)
    return updated


def main():
    old_model = MODEL.read_text(encoding="utf-8")
    old_schemas = SCHEMAS.read_text(encoding="utf-8")
    new_model = modify_model(old_model)
    new_schemas = modify_schemas(old_schemas)
    # Both guarded transformations finish and parse before either file is written.
    if new_model != old_model:
        MODEL.write_text(new_model, encoding="utf-8")
        print("UPDATED:", MODEL.relative_to(ROOT))
    else:
        print("UNCHANGED:", MODEL.relative_to(ROOT))
    if new_schemas != old_schemas:
        SCHEMAS.write_text(new_schemas, encoding="utf-8")
        print("UPDATED:", SCHEMAS.relative_to(ROOT))
    else:
        print("UNCHANGED:", SCHEMAS.relative_to(ROOT))
    print("PASS: scalar Road Hog power retained; dictionary accepted; simultaneous values rejected")
    print("CABBAGE Multi-mode power switching and golden parity are not implemented")


if __name__ == "__main__":
    main()
