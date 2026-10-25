#!/usr/bin/env python3
"""Add the old base platform step to unit production. No fleet changes yet."""
from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parents[2]
MODEL = ROOT / 'src/road_vehicle/model_def.py'
CATALOGUE = ROOT / 'src/road_vehicle/catalogue.py'
UNITS = ROOT / 'src/road_vehicle/units.py'


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

print('PASS: platform support installed; no vehicle definitions or pipelines edited')

# Write after all source guards have passed. Never leave a half-applied stage.
for path, content in pending.items():
    path.write_text(content, encoding="utf-8")
    print("UPDATED:", path.relative_to(ROOT))
