#!/usr/bin/env python3
"""Port verified legacy schema properties and check Stage 005 output.

CABBAGE This is a bounded semantic port. It does not claim fleet/NML parity.
CABBAGE No vehicle files, legacy classes, or graphics code are touched.
"""
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEGACY = ROOT / 'src/road_vehicle/__init__.py'
SCHEMAS = ROOT / 'src/road_vehicle/schemas.py'
REPORT = ROOT / 'migration_state/reports/schema_stage_006.json'
START = '# CABBAGE BEGIN SCHEMA BEHAVIOUR STAGE 006'
END = '# CABBAGE END SCHEMA BEHAVIOUR STAGE 006'

# Only the class-specific overrides genuinely present in legacy classes.
PASSENGER_SUFFIXES = {
    'PaxLocalTram': 'STR_NAME_SUFFIX_PASSENGER_TRAM',
    'PaxExpressCoach': 'STR_NAME_SUFFIX_COACH',
}


def class_nodes(tree):
    return {node.name: node for node in tree.body if isinstance(node, ast.ClassDef)}


def methods(cls):
    return {node.name: node for node in cls.body if isinstance(node, ast.FunctionDef)}


def validate_legacy(tree):
    classes = class_nodes(tree)
    expected = {
        'PaxLocalBusConsist': 'STR_NAME_SUFFIX_BUS',
        'PaxLocalTramConsist': 'STR_NAME_SUFFIX_PASSENGER_TRAM',
        'PaxExpressCoachConsist': 'STR_NAME_SUFFIX_COACH',
    }
    for name, suffix in expected.items():
        method = methods(classes[name])['name_type_suffix']
        returns = [n.value.value for n in ast.walk(method) if isinstance(n, ast.Return) and isinstance(n.value, ast.Constant) and isinstance(n.value.value, str)]
        if returns != [suffix]:
            raise RuntimeError('legacy passenger naming changed: ' + name)
    for name in ('track_type', 'get_expression_for_road_or_tram_type', 'sound_effect'):
        if name not in methods(classes['Consist']):
            raise RuntimeError('legacy property missing: ' + name)
    return classes



def fix_bus_sound_override(source):
    """Keep Bus's legacy departure sound compatible with the read-only property.

    CABBAGE The initializer and property must be installed as one schema stage.
    CABBAGE Inspect AST rather than spelling/whitespace because Black runs often.
    """
    classes = class_nodes(ast.parse(source))
    base = classes['RoadVehicleBase']
    bus = classes['Bus']
    sound_method = methods(base).get('sound_effect')
    if sound_method is None or not any(
        isinstance(d, ast.Name) and d.id == 'property'
        for d in sound_method.decorator_list
    ):
        raise RuntimeError('Stage 006 sound_effect property missing or not read-only')
    if not any(
        isinstance(n, ast.Attribute) and n.attr == '_sound_effect'
        for n in ast.walk(sound_method)
    ):
        raise RuntimeError('sound_effect property is not backed by _sound_effect')
    bus_init = methods(bus).get('__init__')
    if bus_init is None:
        raise RuntimeError('Bus.__init__ missing')
    assignments = [
        (stmt, target)
        for stmt in ast.walk(bus_init)
        if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1
        for target in stmt.targets
        if isinstance(target, ast.Attribute)
        and isinstance(target.value, ast.Name) and target.value.id == 'self'
        and target.attr in ('sound_effect', '_sound_effect')
    ]
    if len(assignments) != 1:
        raise RuntimeError('Expected exactly one Bus departure sound override')
    statement, target = assignments[0]
    if not isinstance(statement.value, ast.Constant) or statement.value.value != 'SOUND_DEPARTURE_OLD_RV_1':
        raise RuntimeError('Unexpected Bus departure sound override; refusing edit')
    if target.attr == '_sound_effect':
        return source
    lines = source.splitlines(keepends=True)
    line = lines[target.lineno - 1]
    old = 'sound_effect'
    start = target.end_col_offset - len(old)
    end = target.end_col_offset
    if line[start:end] != old or line[:start].rstrip()[-1:] != '.':
        raise RuntimeError('Unexpected Bus sound override source span')
    lines[target.lineno - 1] = line[:start] + '_sound_effect' + line[end:]
    result = ''.join(lines)
    ast.parse(result)
    return result



# CABBAGE Source-based forecast, not a claim that the candidate fleet is ready.
def audit_legacy_dependency_surface(legacy_classes):
    unit_file = ROOT / 'src/road_vehicle/units.py'
    unit_tree = ast.parse(unit_file.read_text())
    new_units = class_nodes(unit_tree)
    legacy_units = ('SteamVehicleUnit', 'DieselVehicleUnit', 'ElectricVehicleUnit')
    expected = {
        'SteamVehicleUnit': ('EFFECT_SPAWN_MODEL_STEAM', 'EFFECT_SPRITE_STEAM', 'STEAM', 'SOUND_FACTORY'),
        'DieselVehicleUnit': ('EFFECT_SPAWN_MODEL_DIESEL', 'EFFECT_SPRITE_DIESEL', 'DIESEL', 'SOUND_DEPARTURE_OLD_RV_1'),
        'ElectricVehicleUnit': ('EFFECT_SPAWN_MODEL_ELECTRIC', 'EFFECT_SPRITE_ELECTRIC', 'ELECTRIC', 'SOUND_POWER_STATION'),
    }
    for name in legacy_units:
        if name not in legacy_classes or name not in new_units:
            raise RuntimeError('Stage 005 power unit not provisioned: ' + name)
        def constants(node):
            return {n.value for n in ast.walk(node) if isinstance(n, ast.Constant) and isinstance(n.value, str)}
        missing = set(expected[name]) - constants(new_units[name])
        if missing:
            raise RuntimeError('Unit behaviour parity incomplete: ' + name + ': ' + repr(sorted(missing)))
    # Identify future parity hazards by comparing legacy Consist method surface.
    schema_classes = class_nodes(ast.parse(SCHEMAS.read_text()))
    old_consist_methods = set(methods(legacy_classes['Consist']))
    new_base_methods = set(methods(schema_classes['RoadVehicleBase']))
    unported = sorted(old_consist_methods - new_base_methods - {'__init__', 'add_unit'})
    old_unit_methods = set(methods(legacy_classes['RoadVehicle']))
    new_unit_methods = set(methods(new_units['RoadVehicleUnit']))
    unit_unported = sorted(old_unit_methods - new_unit_methods - {'__init__'})
    return {
        'validated_unit_types': list(legacy_units),
        'legacy_consist_methods_not_on_new_base': unported,
        'legacy_unit_methods_not_on_new_base': unit_unported,
        'warning': 'Static forecast: differences may be intentional or inherited; audit for NML parity before cutover',
    }

def provision_future_fixed_run_cost_property(source):
    """CABBAGE: expose the Iron Horse ModelDef API without changing Road Hog costs."""
    tree = ast.parse(source)
    base = class_nodes(tree)['RoadVehicleBase']
    if 'fixed_run_cost_points' in methods(base):
        method = methods(base)['fixed_run_cost_points']
        snippet = ast.get_source_segment(source, method) or ''
        if 'model_def.fixed_run_cost_points' not in snippet or 'return 180' not in snippet:
            raise RuntimeError('Existing fixed_run_cost_points property differs; review manually')
        return source
    anchor = '    @property\n    def intro_year(self):\n'
    if source.count(anchor) != 1:
        raise RuntimeError('Cannot identify RoadVehicleBase property insertion anchor')
    return source.replace(anchor,
        '    # CABBAGE: Future Iron Horse fixed running-cost API; deliberately unused\n'
        '    # by the current Road Hog running_cost formula.\n'
        '    @property\n'
        '    def fixed_run_cost_points(self):\n'
        '        if self.model_def.fixed_run_cost_points is not None:\n'
        '            return self.model_def.fixed_run_cost_points\n'
        '        return 180\n\n' + anchor, 1)


def provision_sprite_row_migration_shims(source, legacy_classes):
    '''CABBAGE Port legacy graphics-pipeline interfaces without changing pipelines.

    The new schema intentionally retains no Consist inheritance. Only install
    verified legacy method bodies on RoadVehicleBase. Preserve existing methods.
    '''
    legacy = methods(legacy_classes['Consist'])
    for name in ('unique_units', 'get_spriterows_for_consist_or_subpart'):
        if name not in legacy:
            raise RuntimeError('Missing legacy sprite row contract: ' + name)
    classes = class_nodes(ast.parse(source))
    base = classes['RoadVehicleBase']
    present = methods(base)
    expected = {
        'unique_units': '''    # CABBAGE MIGRATION SHIM: graphics pipelines expect legacy Consist.unique_units.
    # CABBAGE Remove only when graphics consumers use the new model interface.
    @property
    def unique_units(self):
        unique_units = []
        for unit in self.units:
            if unit not in unique_units:
                unique_units.append(unit)
        return unique_units
''',
        'get_spriterows_for_consist_or_subpart': '''    # CABBAGE MIGRATION SHIM: existing graphics pipelines use legacy sprite-row counts.
    # CABBAGE Keep the original row-count semantics for incomplete sprites and cargo.
    def get_spriterows_for_consist_or_subpart(self, units):
        result = []
        for unit in units:
            unit_rows = []
            if unit.always_use_same_spriterow:
                unit_rows.append(("always_use_same_spriterow", 1))
            else:
                unit_rows.extend(self.gestalt_graphics.get_output_row_counts_by_type())
            result.append(unit_rows)
        return result
''',
    }
    absent = []
    for name, fragment in expected.items():
        if name in present:
            actual = present[name]
            expected_method = next(n for n in ast.parse('class T:\n' + fragment).body[0].body if isinstance(n, ast.FunctionDef))
            def normalised(method):
                return ast.dump(method, annotate_fields=True, include_attributes=False)
            if normalised(actual) != normalised(expected_method):
                raise RuntimeError('Existing ' + name + ' differs; refusing to overwrite')
        else:
            absent.append(fragment)
    if not absent:
        return source
    lines = source.splitlines(keepends=True)
    lines[base.end_lineno:base.end_lineno] = ['\n' + '\n'.join(absent)]
    result = ''.join(lines)
    ast.parse(result)
    return result


def main():
    legacy_classes = validate_legacy(ast.parse(LEGACY.read_text()))
    source = SCHEMAS.read_text()
    # The underlying ModelDef field already comes from the Iron Horse foundation.
    # Keep this additive: do not modify the existing Road Hog running-cost formula.
    source = provision_future_fixed_run_cost_property(source)
    source = provision_sprite_row_migration_shims(source, legacy_classes)
    if source.count(START) != source.count(END) or source.count(START) > 1:
        raise RuntimeError('broken/duplicate Stage 006 markers')
    classes = class_nodes(ast.parse(source))
    required = ('RoadVehicleBase', 'Bus', 'PaxLocalTram', 'PaxExpressCoach')
    absent = sorted(set(required) - set(classes))
    if absent:
        raise RuntimeError('Stage 005 schemas missing: ' + ', '.join(absent))
    # A completed prior run is accepted only if its installed methods remain intact.
    if START in source:
        expected_methods = {
            'RoadVehicleBase': ('track_type', 'sound_effect', 'name_type_suffix', 'name', 'get_expression_for_road_or_tram_type', 'unique_units', 'get_spriterows_for_consist_or_subpart'),
            'PaxLocalTram': ('name_type_suffix',),
            'PaxExpressCoach': ('name_type_suffix',),
        }
        for cls_name, names in expected_methods.items():
            missing = set(names) - set(methods(classes[cls_name]))
            if missing:
                raise RuntimeError('Stage 006 marker found, but installed methods missing in ' + cls_name + ': ' + ', '.join(sorted(missing)))
        # CABBAGE: Earlier installer versions accepted the stage marker without
        # persisting newly provisioned migration shims. Compare against disk,
        # not against the already-transformed in-memory source.
        updated = fix_bus_sound_override(source)
        if updated != SCHEMAS.read_text():
            SCHEMAS.write_text(updated)
            print('UPDATED:', SCHEMAS.relative_to(ROOT))
        else:
            print('UNCHANGED:', SCHEMAS.relative_to(ROOT))
        # Fail closed: a PASS must mean the saved class actually has the methods.
        saved = class_nodes(ast.parse(SCHEMAS.read_text()))
        for cls_name, names in expected_methods.items():
            missing = set(names) - set(methods(saved[cls_name]))
            if missing:
                raise RuntimeError('Stage 006 post-write verification failed for '
                                   + cls_name + ': ' + ', '.join(sorted(missing)))
        print('PASS: Stage 006 installed; required sprite-row migration shims verified')
        return
    # Do not replace user changes or accidentally generate competing methods.
    for name in ('track_type', 'sound_effect', 'name_type_suffix', 'name'):
        if name in methods(classes['RoadVehicleBase']):
            raise RuntimeError('already defined on RoadVehicleBase; review before Stage 006: ' + name)
    for name in PASSENGER_SUFFIXES:
        if 'name_type_suffix' in methods(classes[name]):
            raise RuntimeError('already defined on ' + name)
    # Replace an existing known incorrect property only after verifying its structure.
    road_method = methods(classes['RoadVehicleBase'])['get_expression_for_road_or_tram_type']
    expr = ast.get_source_segment(source, road_method)
    # Compare AST, not spacing or quote style: Black rewrites this regularly.
    expected_expr = ast.parse("def f(self):\n    return 'road_type:' + self.base_track_type_name + ';'\n").body[0].body[0].value
    actual_returns = [node for node in road_method.body if isinstance(node, ast.Return)]
    if len(actual_returns) != 1 or ast.dump(actual_returns[0].value) != ast.dump(expected_expr):
        raise RuntimeError('road type expression has changed semantically; refusing edit')
    replacement = '''    @property
    def get_expression_for_road_or_tram_type(self):
        # CABBAGE Legacy Consist distinguishes road and tram NML expressions.
        prefix = 'tram_type:' if self.roadveh_flag_tram else 'road_type:'
        return prefix + self.track_type + ';'
'''
    # Remove original @property decorator and method together.
    start_line = min([road_method.lineno] + [d.lineno for d in road_method.decorator_list])
    lines = source.splitlines(keepends=True)
    lines[start_line - 1:road_method.end_lineno] = [replacement]
    source = ''.join(lines)
    # Keep methods in one marked, class-assignment block: avoids mutating generated
    # class bodies and remains stable if Black reformats them.
    block = '''# CABBAGE BEGIN SCHEMA BEHAVIOUR STAGE 006
# CABBAGE Dynamic method installation is deliberately NOT used: the definitions
# CABBAGE below are added inside their target class bodies by this installer.
# CABBAGE END SCHEMA BEHAVIOUR STAGE 006
'''
    # Insert methods via class-boundaries, not monkeypatching. Reparse after edit.
    addition = {
        'RoadVehicleBase': '''    @property
    def track_type(self):
        # CABBAGE Preserve the legacy electricity-supply roadtype translation.
        if getattr(self, 'requires_electricity_supply', False):
            return {'RAIL': 'ELRL'}[self.base_track_type_name]
        return self.base_track_type_name

    @property
    def sound_effect(self):
        if getattr(self, '_sound_effect', None) is not None:
            return self._sound_effect
        return getattr(self, 'default_sound_effect', None)

    @property
    def name_type_suffix(self):
        return ('STR_NAME_SUFFIX_' + self.name_suffix_consist_type
                + self.name_suffix_vehicle_type)

    @property
    def name(self):
        # CABBAGE Power suffix must be supplied by unit integration in Stage 007.
        # CABBAGE Fail explicitly rather than silently inventing Diesel/Steam.
        suffix = getattr(self, '_power_type_suffix', None)
        if suffix is None:
            raise ValueError('Power suffix not resolved for ' + self.model_def.model_id)
        return ('string(STR_NAME_CONSIST, string(STR_NAME_'
                + self.model_def.model_id.upper() + '), string('
                + self.name_type_suffix + '), string(STR_NAME_SUFFIX_'
                + suffix + '))')

''',
        'PaxLocalTram': '''    @property
    def name_type_suffix(self):
        return 'STR_NAME_SUFFIX_PASSENGER_TRAM'

''',
        'PaxExpressCoach': '''    @property
    def name_type_suffix(self):
        return 'STR_NAME_SUFFIX_COACH'

''',
    }
    for name, fragment in addition.items():
        tree = ast.parse(source)
        cls = class_nodes(tree)[name]
        src_lines = source.splitlines(keepends=True)
        src_lines[cls.end_lineno:cls.end_lineno] = ['\n' + fragment]
        source = ''.join(src_lines)
    # Place comment marker (not behaviour) at EOF, after generated Stage 005 section.
    if START not in source:
        source = source.rstrip() + '\n\n' + block
    source = fix_bus_sound_override(source)
    ast.parse(source)
    if SCHEMAS.read_text() != source:
        SCHEMAS.write_text(source)
        print('UPDATED:', SCHEMAS.relative_to(ROOT))
    else:
        print('UNCHANGED:', SCHEMAS.relative_to(ROOT))
    report = {
        'integrated': ['road/tram type NML selector', 'electric rail track translation', 'legacy sound override fallback', 'Bus read-only sound property compatibility', 'generic legacy vehicle name composition', 'local tram name suffix', 'express coach name suffix'],
        'preserved': ['legacy BasePlatform', 'vehicle modules', 'graphics pipelines', 'Bus.name fixture override'],
        'known_gaps': ['unit power source suffix resolution', 'unit default sound selection', 'schema initialiser parity and model attributes', 'graphics gestalt integration', 'production fleet installation', 'compiled NML and PNG parity'],
        'legacy_class_method_overrides': {k: sorted(methods(v).keys()) for k, v in legacy_classes.items() if k.endswith('Consist') and any(m != '__init__' for m in methods(v))},
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    report['legacy_dependency_audit'] = audit_legacy_dependency_surface(legacy_classes)
    REPORT.write_text(json.dumps(report, indent=2) + '\n')
    print('PASS: schema property integration installed; no production fleet switched')
    print('CABBAGE: Stage 006 is not NML-parity complete; see report')


if __name__ == '__main__':
    main()
