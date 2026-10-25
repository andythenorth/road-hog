#!/usr/bin/env python3
"""Provision base platform, unit interface and ModelDef compatibility defaults."""
from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parents[2]
MODEL = ROOT / 'src/road_vehicle/model_def.py'
CATALOGUE = ROOT / 'src/road_vehicle/catalogue.py'
UNITS = ROOT / 'src/road_vehicle/units.py'


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


def default_sprites_incomplete(source):
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



def mark_deferred_template_support(source):
    """Keep the Pass 2 obligation in permanent ModelDef source, not a report."""
    marker = "# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml."
    if marker in source:
        return source
    cls = only_class(source, "ModelDef")
    fields = [n for n in cls.body if isinstance(n, ast.AnnAssign)
              and isinstance(n.target, ast.Name) and n.target.id == "sprites_complete"]
    if len(fields) != 1:
        raise RuntimeError("Cannot uniquely locate ModelDef.sprites_complete")
    lines = source.splitlines(keepends=True)
    line = lines[fields[0].lineno - 1]
    indent = line[:len(line) - len(line.lstrip())]
    lines.insert(fields[0].lineno - 1,
        indent + marker + "\n"
        + indent + "# CABBAGE FUTURE PASS: restore legacy per-vehicle template selection,\n"
        + indent + "# cargo-specific spritegroups and livery behaviour; audit affected vehicles.\n")
    result = "".join(lines)
    ast.parse(result)
    return result


pending = {}

def patch(path, before, after):
    text = pending.get(path, path.read_text(encoding='utf-8'))
    if after in text:
        print('UNCHANGED:', path.relative_to(ROOT))
        return
    if text.count(before) != 1:
        raise SystemExit(f'FAIL: unexpected source in {path}; expected one exact match, got {text.count(before)}')
    pending[path] = text.replace(before, after)
    print('PLANNED:', path.relative_to(ROOT))


# A platform can provide the unit class, so make the fallback base unit explicit.
patch(MODEL,
    '    unit_cls_name: str\n',
    '    unit_cls_name: str = \"RoadVehicleUnit\"\n')
patch(MODEL,
    '    reverse_sprite_template: bool = False\n',
    '    reverse_sprite_template: bool = False\n'
    '    # CABBAGE Road Hog platform classes are still the old source of shared tractor/chassis props.\n'
    '    base_platform: Optional[Any] = None\n'
    '    # BasePlatform has a few old unit fields that Horse UnitDef did not need.\n'
    '    always_use_same_spriterow: bool = False\n'
    '    cargo_length: Optional[int] = None\n'
    '    semi_truck_shift_offset_jank: Optional[int] = None\n'
    '    unit_is_semi_tractor: bool = False\n')

# CABBAGE There are two known formatting styles of this exact producer loop.
# Replace the whole loop once, rather than matching its whitespace line by line.
import re

catalogue_text = pending.get(CATALOGUE, CATALOGUE.read_text(encoding='utf-8'))
loop_pattern = re.compile(
    r"        for counter,\s*unit_def in enumerate\(self\.catalogue\.model_def\.unit_defs\):\n"
    r"(?:            .*\n)+?"
    r"            for _ in range\(unit_def\.repeat\):\n"
    r"                model_variant\.units\.append\(unit\)\n"
)
match = loop_pattern.search(catalogue_text)
new_loop = """        for counter, unit_def in enumerate(self.catalogue.model_def.unit_defs):
            # CABBAGE Keep old platform override order, including the legacy `type` field.
            # Resolve once per UnitDef; repeated physical units reuse the same object.
            from dataclasses import replace
            resolved_def = unit_def
            platform = None
            if unit_def.base_platform is not None:
                platform = unit_def.base_platform()
                configured = platform.configure_unit_args(
                    **{key: value for key, value in vars(unit_def).items() if key != "base_platform"}
                )
                platform_unit_type = configured.pop("type", None)
                configured.pop("base_platform", None)
                if platform_unit_type is not None:
                    configured["unit_cls_name"] = platform_unit_type.__name__
                resolved_def = replace(unit_def, **configured)
            unit_cls = getattr(units, resolved_def.unit_cls_name)
            unit = unit_cls(
                model_variant=model_variant,
                unit_def=resolved_def,
                id=catalogue_entry.unit_variant_ids[counter],
                numeric_id=catalogue_entry.unit_numeric_ids[counter],
            )
            if platform is not None:
                unit.base_platform = platform
            for _ in range(unit_def.repeat):
                model_variant.units.append(unit)
"""
if new_loop not in catalogue_text:
    if match is None or catalogue_text.count(match.group()) != 1:
        raise SystemExit(f"FAIL: unexpected unit producer loop in {CATALOGUE}")
    old_loop = match.group()
    if not ("unit_cls" in old_loop and "numeric_id=catalogue_entry.unit_numeric_ids[counter]" in old_loop):
        raise SystemExit("FAIL: unit producer structure has changed; refusing replacement")
    pending[CATALOGUE] = catalogue_text.replace(old_loop, new_loop)
    print('PLANNED:', CATALOGUE.relative_to(ROOT))
else:
    print('UNCHANGED:', CATALOGUE.relative_to(ROOT))
# The unit initializer may have been formatted by Black. Match assignment syntax,
# not the original spaces around '='. Keep each guard strict so it fails safely.
units_text = pending.get(UNITS, UNITS.read_text(encoding="utf-8"))
marker = "# The producer sets the resolved platform instance when there is one."
if marker not in units_text:
    anchor = re.compile(r"^(?P<indent>[ \t]+)self\.unit_def\s*=\s*unit_def[ \t]*$", re.M)
    matches = list(anchor.finditer(units_text))
    if len(matches) != 1:
        raise SystemExit(f"FAIL: expected exactly one self.unit_def assignment in {UNITS}; got {len(matches)}")
    match = matches[0]
    indent = match.group("indent")
    extra = "\n".join(indent + line for line in (
        "# The producer sets the resolved platform instance when there is one.",
        "self.base_platform = None",
        "self.always_use_same_spriterow = bool(unit_def.always_use_same_spriterow)",
        "self.unit_is_semi_tractor = bool(unit_def.unit_is_semi_tractor)",
        "self.semi_truck_shift_offset_jank = unit_def.semi_truck_shift_offset_jank",
        "self.cargo_length = unit_def.cargo_length",
    ))
    units_text = units_text[:match.end()] + "\n" + extra + units_text[match.end():]

# Remove old constructor defaults. Otherwise they overwrite platform settings.
# Only touch the RoadVehicleUnit initializer, never another method/class.
parsed = ast.parse(units_text)
base = next((n for n in parsed.body if isinstance(n, ast.ClassDef) and n.name == "RoadVehicleUnit"), None)
initializer = next((n for n in base.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == "__init__"), None) if base else None
if initializer is None:
    raise SystemExit(f"FAIL: RoadVehicleUnit.__init__ not found in {UNITS}")
lines = units_text.splitlines(keepends=True)
old_fields = {
    "semi_truck_shift_offset_jank": "None",
    "always_use_same_spriterow": "False",
    "unit_is_semi_tractor": "False",
}
# AST distinguishes the new assignments from the old ones even after Black.
remove_lines = []
for node in initializer.body:
    if not isinstance(node, ast.Assign) or len(node.targets) != 1:
        continue
    target = node.targets[0]
    if not isinstance(target, ast.Attribute) or not isinstance(target.value, ast.Name) or target.value.id != "self":
        continue
    expected = old_fields.get(target.attr)
    if expected is None:
        continue
    is_old_default = (isinstance(node.value, ast.Constant) and
        ((expected == "None" and node.value.value is None) or
         (expected == "False" and node.value.value is False)))
    if is_old_default:
        remove_lines.extend(range(node.lineno, node.end_lineno + 1))
if len(remove_lines) != 3:
    # If the old defaults are already gone, the earlier patch was installed.
    if len(remove_lines) != 0:
        raise SystemExit(f"FAIL: only {len(remove_lines)} of 3 old unit defaults found; refusing partial change")
else:
    for line_number in sorted(remove_lines, reverse=True):
        del lines[line_number - 1]
units_text = "".join(lines)
ast.parse(units_text)
if units_text != UNITS.read_text(encoding="utf-8"):
    pending[UNITS] = units_text
    print("PLANNED:", UNITS.relative_to(ROOT))
else:
    print("UNCHANGED:", UNITS.relative_to(ROOT))
# CABBAGE MIGRATION SHIM: the unchanged graphics pipeline accesses unit.chassis.
# UnitDef remains the single source of truth; do not copy chassis state.
parsed = ast.parse(units_text)
base = next((n for n in parsed.body if isinstance(n, ast.ClassDef) and n.name == "RoadVehicleUnit"), None)
if base is None:
    raise SystemExit(f"FAIL: RoadVehicleUnit missing in {UNITS}")
methods = [n for n in base.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == "chassis"]
if len(methods) > 1:
    raise SystemExit("FAIL: ambiguous duplicate chassis properties")
if methods:
    method = methods[0]
    if not any(isinstance(d, ast.Name) and d.id == 'property' for d in method.decorator_list):
        raise SystemExit("FAIL: existing chassis method is not a property")
    expected_body = ast.parse("def chassis(self):\n    return self.unit_def.chassis").body[0].body
    if ast.dump(ast.Module(body=method.body, type_ignores=[]), include_attributes=False) != ast.dump(ast.Module(body=expected_body, type_ignores=[]), include_attributes=False):
        raise SystemExit("FAIL: existing chassis property has different semantics")
else:
    init = next((n for n in base.body if isinstance(n, ast.FunctionDef) and n.name == '__init__'), None)
    if init is None or init.end_lineno is None:
        raise SystemExit("FAIL: RoadVehicleUnit initializer missing")
    lines = units_text.splitlines(keepends=True)
    addition = ("\n"
                "    @property\n"
                "    def chassis(self):\n"
                "        # CABBAGE MIGRATION SHIM: legacy pipeline expects unit.chassis.\n"
                "        return self.unit_def.chassis\n")
    lines.insert(init.end_lineno, addition)
    units_text = ''.join(lines)
    ast.parse(units_text)
    pending[UNITS] = units_text
    print('PLANNED:', UNITS.relative_to(ROOT), 'CABBAGE chassis property')

# CABBAGE Infrastructure owner: scalar power + sprite completeness defaults.
# Former standalone stages 009 and 010 are consolidated here. All source
# guards execute before any source file is written.
model_text = pending.get(MODEL, MODEL.read_text(encoding='utf-8'))
model_text = mark_deferred_template_support(default_sprites_incomplete(modify_model(model_text)))
if model_text != MODEL.read_text(encoding='utf-8'):
    pending[MODEL] = model_text
    print('PLANNED:', MODEL.relative_to(ROOT), 'power and sprites defaults')

schemas_path = ROOT / 'src/road_vehicle/schemas.py'
schemas_text = modify_schemas(schemas_path.read_text(encoding='utf-8'))
if schemas_text != schemas_path.read_text(encoding='utf-8'):
    pending[schemas_path] = schemas_text
    print('PLANNED:', schemas_path.relative_to(ROOT), 'scalar power behaviour')

for candidate in pending.values():
    ast.parse(candidate)

print('PASS: platform, scalar power and incomplete sprite defaults prepared; no fleet or graphics edits')

# Write after all source guards have passed. Never leave a half-applied stage.
for path, content in pending.items():
    path.write_text(content, encoding="utf-8")
    print("UPDATED:", path.relative_to(ROOT))
