#!/usr/bin/env python3
"""Provision Road Hog fleet schemas from the actual legacy class bodies.

CABBAGE This ports initialiser configuration, not complete rendering behaviour.
CABBAGE Do not switch the production fleet before output parity has been checked.
"""
import ast
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEGACY = ROOT / 'src/road_vehicle/__init__.py'
TARGET = ROOT / 'src/road_vehicle/schemas.py'
REPORT = ROOT / 'migration_state/reports/schema_stage_005.json'
START = '# CABBAGE BEGIN GENERATED FLEET SCHEMAS STAGE 005'
END = '# CABBAGE END GENERATED FLEET SCHEMAS STAGE 005'


def produce(legacy_source):
    tree = ast.parse(legacy_source)
    classes = {n.name:n for n in tree.body if isinstance(n, ast.ClassDef)}
    track = [name for name in classes if name.startswith('TrackTypeMixin') and name != 'TrackTypeMixinBase']
    bases = [name for name in classes if name.endswith('ConsistBase') and name != 'Consist']
    # Include MetalHEQSBase (its name does not end in ConsistBase).
    concrete = [name for name in classes if name.endswith('Consist') and name != 'Consist']
    concrete += ['MetalHEQSBase']
    lines = [START, 'import polar_fox', 'import gestalt_graphics.graphics_constants as graphics_constants',
             'from gestalt_graphics.gestalt_graphics import (GestaltGraphicsVisibleCargo, GestaltGraphicsLiveryOnly, GestaltGraphicsCustom)',
             '', '# CABBAGE The original track mixins use class attributes; keep that composition.']
    # CABBAGE Restore the legacy track mixin base so inherited defaults resolve.
    base_node = classes['TrackTypeMixinBase']
    lines.append('class TrackTypeMixinBase:')
    for statement in base_node.body:
        if isinstance(statement, (ast.Assign, ast.AnnAssign)):
            lines.append('    ' + ast.unparse(statement).replace('\n', '\n    '))
    lines.append('')
    for name in track:
        node = classes[name]
        lines.append(f'class {name}(TrackTypeMixinBase):')
        assignments = [n for n in node.body if isinstance(n, (ast.Assign, ast.AnnAssign))]
        if not assignments:
            lines.append('    pass')
        for statement in assignments:
            lines.append('    ' + ast.unparse(statement).replace('\n','\n    '))
        lines.append('')
    # Base classes: copy their initialiser configuration, retaining the sequence of overrides.
    for name in bases:
        node = classes[name]
        parents = [n.id for n in node.bases if isinstance(n, ast.Name)]
        parent = next((p for p in parents if p in bases), 'RoadVehicleBase')
        lines.extend([f'class {name}({parent}):', '    def __init__(self, producer, catalogue_entry):', '        super().__init__(producer, catalogue_entry)'])
        init = next((n for n in node.body if isinstance(n, ast.FunctionDef) and n.name == '__init__'), None)
        if init:
            for s in init.body:
                if isinstance(s, ast.Expr) and isinstance(s.value, ast.Call) and isinstance(s.value.func, ast.Attribute) and s.value.func.attr == '__init__':
                    continue
                if isinstance(s, ast.Expr) and isinstance(s.value, ast.Call) and isinstance(s.value.func, ast.Attribute) and isinstance(s.value.func.value, ast.Call) and isinstance(s.value.func.value.func, ast.Name) and s.value.func.value.func.id == 'super':
                    continue
                lines.append('        ' + ast.unparse(s).replace('\n', '\n        '))
        lines.append('')
    for name in concrete:
        node = classes[name]
        parents = [n.id for n in node.bases if isinstance(n, ast.Name)]
        cargo_parent = next((p for p in parents if p in bases), 'RoadVehicleBase')
        mixin = next((p for p in parents if p in track), None)
        out_name = name[:-7] if name.endswith('Consist') else name
        # Keep Bus as the independently validated migration fixture.
        if name == 'PaxLocalBusConsist':
            continue
        lines.append(f'class {out_name}({cargo_parent}):')
        lines.append('    def __init__(self, producer, catalogue_entry):')
        lines.append('        super().__init__(producer, catalogue_entry)')
        if mixin:
            for key in ('base_track_type_name','roadveh_flag_tram','tractive_effort_coefficient','name_suffix_vehicle_type','vehicle_role'):
                lines.append(f'        self.{key} = {mixin}.{key}')
        init = next((n for n in node.body if isinstance(n, ast.FunctionDef) and n.name == '__init__'), None)
        if init:
            for s in init.body:
                if isinstance(s, ast.Expr) and isinstance(s.value, ast.Call) and isinstance(s.value.func, ast.Attribute) and isinstance(s.value.func.value, ast.Call) and isinstance(s.value.func.value.func, ast.Name) and s.value.func.value.func.id == 'super':
                    continue
                lines.append('        '+ast.unparse(s).replace('\n','\n        '))
        lines.append('')
    lines.append(END)
    result='\n'.join(lines)+'\n'
    ast.parse(result)
    return result, {'track_mixins':track,'cargo_bases':bases,'concrete_classes':[n[:-7] if n.endswith('Consist') else n for n in concrete if n != 'PaxLocalBusConsist'], 'known_gaps':['legacy properties / methods beyond __init__ not yet ported', 'schema naming parity and registration', 'render and sprite regression', 'legacy defaults inherited from Consist not all represented', 'complete fleet definition conversion']}


def repair_existing_mixins(source, mixins):
    """Restore the missing class parent, preserving all other source verbatim."""
    before, rest = source.split(START, 1)
    middle, after = rest.split(END, 1)
    block = START + middle + END
    tree = ast.parse(block)
    classes = {n.name: n for n in tree.body if isinstance(n, ast.ClassDef)}
    if 'TrackTypeMixinBase' in classes:
        base = classes['TrackTypeMixinBase']
        attrs = {t.id for n in base.body if isinstance(n, ast.Assign) for t in n.targets if isinstance(t, ast.Name)}
        if not {'base_track_type_name','roadveh_flag_tram','tractive_effort_coefficient','name_suffix_vehicle_type','vehicle_role'} <= attrs:
            raise RuntimeError('TrackTypeMixinBase has unexpected attributes')
    else:
        legacy_tree = ast.parse(LEGACY.read_text())
        legacy = next(n for n in legacy_tree.body if isinstance(n,ast.ClassDef) and n.name=='TrackTypeMixinBase')
        assignments = [n for n in legacy.body if isinstance(n,(ast.Assign,ast.AnnAssign))]
        definitions = ['class TrackTypeMixinBase:'] + ['    ' + ast.unparse(n).replace('\n','\n    ') for n in assignments]
        insert = '\n'.join(definitions) + '\n\n'
        match = re.search(r'(?m)^class TrackTypeMixin(?:Cake|Feldbahn|HEQS|Tram|TruckBusCoach)\s*(?:\([^\n]*\))?:',block)
        if not match:
            raise RuntimeError('track mixins not found in installed block')
        block = block[:match.start()] + insert + block[match.start():]
    for mixin in mixins:
        pattern = rf'(?m)^class {re.escape(mixin)}(?:\(([^\n]*)\))?:'
        matches = list(re.finditer(pattern, block))
        if len(matches) != 1:
            raise RuntimeError(f'Expected one {mixin} declaration, found {len(matches)}')
        parents = matches[0].group(1)
        if parents not in (None, 'TrackTypeMixinBase'):
            raise RuntimeError(f'Unexpected parents of {mixin}: {parents}')
        block = re.sub(pattern, f'class {mixin}(TrackTypeMixinBase):', block, count=1)
    result = before + block + after
    ast.parse(result, filename=str(TARGET))
    return result


#!/usr/bin/env python3
"""Install legacy steam/diesel/electric unit behaviour in the new unit module.

CABBAGE: bounded unit compatibility port; graphics pipeline and vehicles untouched.
"""
import ast
from pathlib import Path

UNIT_ROOT = Path(__file__).resolve().parents[2]
UNIT_LEGACY = UNIT_ROOT / 'src/road_vehicle/__init__.py'
UNIT_TARGET = UNIT_ROOT / 'src/road_vehicle/units.py'
UNIT_START = '# CABBAGE BEGIN LEGACY UNIT TYPES STAGE 005'
UNIT_END = '# CABBAGE END LEGACY UNIT TYPES STAGE 005'

UNIT_ADDITION = """
# CABBAGE BEGIN LEGACY UNIT TYPES STAGE 005
# CABBAGE Port unit-originating effects and consist state, not unit aliases.
# DieselVehicleUnit exists already; restore its missing model side effects.
class SteamVehicleUnit(RoadVehicleUnit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._effect_spawn_model = "EFFECT_SPAWN_MODEL_STEAM"
        self.default_effect_sprite = "EFFECT_SPRITE_STEAM"
        self.model_variant._power_type_suffix = "STEAM"
        self.model_variant.default_sound_effect = "SOUND_FACTORY"


class ElectricVehicleUnit(RoadVehicleUnit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_variant.requires_electricity_supply = True
        self._effect_spawn_model = "EFFECT_SPAWN_MODEL_ELECTRIC"
        self.default_effect_sprite = "EFFECT_SPRITE_ELECTRIC"
        self.model_variant._power_type_suffix = "ELECTRIC"
        self.model_variant.default_sound_effect = "SOUND_POWER_STATION"
# CABBAGE END LEGACY UNIT TYPES STAGE 005
"""


def unit_class_nodes(source):
    return {n.name: n for n in ast.parse(source).body if isinstance(n, ast.ClassDef)}


def provision_power_units():
    original = UNIT_TARGET.read_text()
    legacy = UNIT_LEGACY.read_text()
    old = unit_class_nodes(legacy)
    for name in ('SteamVehicleUnit', 'DieselVehicleUnit', 'ElectricVehicleUnit'):
        if name not in old:
            raise RuntimeError('Legacy class not found: ' + name)
    # Guard exact source-derived per-type side effects before applying the port.
    legacy_expect = {
        'SteamVehicleUnit': ('EFFECT_SPAWN_MODEL_STEAM', 'EFFECT_SPRITE_STEAM', 'STEAM', 'SOUND_FACTORY'),
        'DieselVehicleUnit': ('EFFECT_SPAWN_MODEL_DIESEL', 'EFFECT_SPRITE_DIESEL', 'DIESEL', 'SOUND_DEPARTURE_OLD_RV_1'),
        'ElectricVehicleUnit': ('EFFECT_SPAWN_MODEL_ELECTRIC', 'EFFECT_SPRITE_ELECTRIC', 'ELECTRIC', 'SOUND_POWER_STATION'),
    }
    for name, values in legacy_expect.items():
        cls = old[name]
        text = ast.get_source_segment(legacy, cls)
        if not all(repr(v) in text or ('"' + v + '"') in text for v in values):
            raise RuntimeError('Legacy semantics changed: ' + name)
    found = unit_class_nodes(original)
    if 'RoadVehicleUnit' not in found or 'DieselVehicleUnit' not in found:
        raise RuntimeError('Unexpected unit class hierarchy')
    if UNIT_START in original or UNIT_END in original:
        if original.count(UNIT_START) == original.count(UNIT_END) == 1 and all(n in found for n in ('SteamVehicleUnit', 'ElectricVehicleUnit')):
            print('PASS: Stage 005 unit types already installed')
            return
        raise RuntimeError('Partial or inconsistent Stage 005 installation')
    if any(n in found for n in ('SteamVehicleUnit', 'ElectricVehicleUnit')):
        raise RuntimeError('Conflicting specialised unit implementation; refusing overwrite')
    diesel = found['DieselVehicleUnit']
    if not diesel.body or not isinstance(diesel.body[0], ast.FunctionDef):
        raise RuntimeError('Unexpected diesel constructor')
    init = diesel.body[0]
    if init.name != '__init__' or not any(isinstance(n, ast.Constant) and n.value == 'EFFECT_SPRITE_DIESEL' for n in ast.walk(init)):
        raise RuntimeError('Unexpected existing diesel implementation')
    if any(isinstance(n, ast.Attribute) and n.attr == '_power_type_suffix' for n in ast.walk(init)):
        raise RuntimeError('Diesel already sets suffix; inspect existing implementation')
    # Append after the existing constructor, within its body (AST-validated, whitespace-safe).
    lines = original.splitlines(keepends=True)
    insert_at = init.end_lineno
    indent = ' ' * (init.col_offset + 4)
    diesel_extra = (indent + '# CABBAGE Stage 005: restore legacy unit-originating model defaults.\n'
                    + indent + 'self.model_variant._power_type_suffix = "DIESEL"\n'
                    + indent + 'self.model_variant.default_sound_effect = "SOUND_DEPARTURE_OLD_RV_1"\n')
    # Diesel class is final in the original module; reject unexpected intervening source.
    if any(line.strip() for line in lines[insert_at:]):
        raise RuntimeError('Unexpected content after DieselVehicleUnit; refusing insertion')
    result = ''.join(lines[:insert_at]) + ('\n' if lines[insert_at - 1] and not lines[insert_at - 1].endswith('\n') else '') + diesel_extra + '\n' + UNIT_ADDITION + '\n'
    ast.parse(result)
    updated = unit_class_nodes(result)
    if not all(n in updated for n in legacy_expect):
        raise RuntimeError('Incomplete unit class provision')
    UNIT_TARGET.write_text(result)
    print('UPDATED: src/road_vehicle/units.py')
    print('PASS: three distinct power unit types; legacy effects and model defaults restored')



def ensure_base_loading_speed_default(source):
    """CABBAGE: Legacy Consist defaults this to 1; child schemas may override."""
    tree = ast.parse(source)
    base = next((n for n in tree.body if isinstance(n, ast.ClassDef)
                 and n.name == 'RoadVehicleBase'), None)
    if base is None:
        raise RuntimeError('RoadVehicleBase missing')
    init = next((n for n in base.body if isinstance(n, ast.FunctionDef)
                 and n.name == '__init__'), None)
    if init is None:
        raise RuntimeError('RoadVehicleBase.__init__ missing')
    assignments = []
    for statement in init.body:
        if isinstance(statement, (ast.Assign, ast.AnnAssign)):
            targets = statement.targets if isinstance(statement, ast.Assign) else [statement.target]
            if any(isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name)
                   and target.value.id == 'self' and target.attr == 'loading_speed_multiplier'
                   for target in targets):
                assignments.append(statement)
    if assignments:
        if len(assignments) != 1 or not isinstance(assignments[0].value, ast.Constant) or assignments[0].value.value != 1:
            raise RuntimeError('Existing RoadVehicleBase loading-speed assignment differs from legacy default')
        return source
    # Insert inside __init__ at a bounded, source-verified anchor without reformatting.
    lines = source.splitlines(keepends=True)
    anchor_index = next((i for i in range(init.lineno - 1, init.end_lineno)
                         if 'self.vehicle_life = 40' in lines[i]), None)
    if anchor_index is None:
        raise RuntimeError('Cannot locate RoadVehicleBase loading-speed default anchor')
    lines.insert(anchor_index + 1,
                 '        # CABBAGE MIGRATION SHIM: legacy Consist default; child schemas override as needed.\n'
                 '        self.loading_speed_multiplier = 1\n')
    result = ''.join(lines)
    verify_base_loading_speed_default(result)
    return result


def verify_base_loading_speed_default(source):
    tree = ast.parse(source)
    base = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'RoadVehicleBase')
    init = next(n for n in base.body if isinstance(n, ast.FunctionDef) and n.name == '__init__')
    found = [n for n in init.body if isinstance(n, ast.Assign)
             and any(isinstance(t, ast.Attribute) and isinstance(t.value, ast.Name)
                     and t.value.id == 'self' and t.attr == 'loading_speed_multiplier'
                     for t in n.targets)]
    if len(found) != 1 or not isinstance(found[0].value, ast.Constant) or found[0].value.value != 1:
        raise RuntimeError('Stage 005 failed to persist legacy loading-speed default')


def main():
    old = LEGACY.read_text()
    target = TARGET.read_text()
    if target.count(START) != target.count(END):
        raise RuntimeError('unbalanced stage 005 markers')
    if target.count(START) > 1:
        raise RuntimeError('duplicate stage 005 markers')
    block, report = produce(old)
    if START in target:
        # CABBAGE Existing stage 006 can have added methods inside the generated block.
        # Do not regenerate and lose those methods. Repair only mixin inheritance.
        new = repair_existing_mixins(target, report['track_mixins'])
    else:
        new = target.rstrip()+'\n\n'+block
    new = ensure_base_loading_speed_default(new)
    ast.parse(new, filename=str(TARGET))
    # Fail closed if existing name collisions would overwrite the validated bus.
    original = ast.parse(target.split(START,1)[0])
    existing = {n.name for n in original.body if isinstance(n,ast.ClassDef)}
    added = set(report['concrete_classes']) | set(report['cargo_bases']) | set(report['track_mixins']) | {'TrackTypeMixinBase'}
    collision = existing & added
    if collision:
        raise RuntimeError('existing schema collision: '+repr(sorted(collision)))
    if new != target:
        TARGET.write_text(new)
        print('UPDATED:', TARGET.relative_to(ROOT))
    else:
        print('UNCHANGED:', TARGET.relative_to(ROOT))
    verify_base_loading_speed_default(TARGET.read_text())
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    REPORT.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: schema initialisers provisioned; production vehicle definitions unchanged')
    print('Concrete schemas:', len(report['concrete_classes']),'cargo bases:',len(report['cargo_bases']))
    provision_power_units()
    print('CABBAGE: This is a schema foundation, NOT a compiled fleet or NML parity pass')

if __name__ == '__main__':
    main()
