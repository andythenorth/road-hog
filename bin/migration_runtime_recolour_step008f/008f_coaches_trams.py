#!/usr/bin/env python3
"""008f: Three existing runtime-recolour catalogue liveries on coaches and pax trams.

Run from the Road Hog repository root. Deterministic and safe to rerun.
"""
import ast
from pathlib import Path

ROOT = Path.cwd()
VEHICLES = ROOT / 'src' / 'vehicles'
SCHEMAS = ROOT / 'src' / 'road_vehicle' / 'schemas.py'
LIVERIES = (
    'RANDOM_LIVERIES_COMPLEMENT_COMPANY_COLOUR',
    'RANDOM_LIVERIES_CLOVER_OCHRE_SULPHUR',
    'RANDOM_LIVERIES_TEAL_PEWTER_SILVER',
)
TARGETS = {
    'acton_pax_express': ('PaxExpressCoach', 'PaxExpressCoachRuntimeRemapSpike', 600),
    'big_sky_pax_express': ('PaxExpressCoach', 'PaxExpressCoachRuntimeRemapSpike', 620),
    'glenmore_pax_express': ('PaxExpressCoach', 'PaxExpressCoachRuntimeRemapSpike', 50),
    'oxleas_pax_express': ('PaxExpressCoach', 'PaxExpressCoachRuntimeRemapSpike', 610),
    'fairlop_pax': ('PaxLocalTram', 'PaxLocalTramRuntimeRemapSpike', 10),
    'ladycross_pax': ('PaxLocalTram', 'PaxLocalTramRuntimeRemapSpike', 0),
    'newbold_pax': ('PaxLocalTram', 'PaxLocalTramRuntimeRemapSpike', 30),
    'northbeach_pax': ('PaxLocalTram', 'PaxLocalTramRuntimeRemapSpike', 690),
    'twinhills_pax': ('PaxLocalTram', 'PaxLocalTramRuntimeRemapSpike', 70),
}
SCHEMA_ADDITION = '''\n\nclass PaxLocalTramRuntimeRemapSpike(PaxLocalTram):
    # CABBAGE352 008f: explicit runtime-remap graphics selection for pax trams.
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.gestalt_graphics = GestaltGraphicsSimpleBodyColourRemaps()
\n\nclass PaxExpressCoachRuntimeRemapSpike(PaxExpressCoach):
    # CABBAGE352 008f: explicit runtime-remap graphics selection for coaches.
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.gestalt_graphics = GestaltGraphicsSimpleBodyColourRemaps()
'''


def model_call(path, source):
    tree = ast.parse(source, filename=str(path))
    matches = [n for n in ast.walk(tree) if isinstance(n, ast.Call)
               and isinstance(n.func, ast.Name) and n.func.id == 'ModelDef']
    if len(matches) != 1:
        raise RuntimeError(f'{path}: expected one ModelDef')
    return {kw.arg: kw.value for kw in matches[0].keywords}


def update_model(path, original, replacement, numeric_id):
    source = path.read_text()
    kw = model_call(path, source)
    if ast.literal_eval(kw['base_numeric_id']) != numeric_id:
        raise RuntimeError(f'{path}: base numeric ID differs from reviewed source')
    old_schema = ast.literal_eval(kw['schema_name'])
    if old_schema not in (original, replacement):
        raise RuntimeError(f'{path}: unexpected schema {old_schema}')
    if 'liveries' in kw:
        if tuple(ast.literal_eval(kw['liveries'])) != LIVERIES:
            raise RuntimeError(f'{path}: existing liveries conflict')
    else:
        name = ast.literal_eval(kw['name'])
        anchor = f'        name="{name}",'
        if source.count(anchor) != 1:
            raise RuntimeError(f'{path}: name anchor changed')
        addition = anchor + '\n        # CABBAGE352 008f: catalogue runtime colour variants.\n        liveries=[\n'
        addition += ''.join(f'            "{name}",\n' for name in LIVERIES)
        addition += '        ],'
        source = source.replace(anchor, addition)
    anchor = f'schema_name="{original}",'
    replacement_text = f'schema_name="{replacement}",'
    if replacement_text not in source:
        if source.count(anchor) != 1:
            raise RuntimeError(f'{path}: missing original schema anchor')
        source = source.replace(anchor, replacement_text)
    if source.count(replacement_text) != 1:
        raise RuntimeError(f'{path}: schema selection not unique')
    return source


def main():
    schema_source = SCHEMAS.read_text()
    if 'class PaxLocalBusRuntimeRemapSpike(PaxLocalBus)' not in schema_source:
        raise RuntimeError('008c/008e bus runtime schema missing')
    if 'class GestaltGraphicsSimpleBodyColourRemaps' not in (ROOT / 'src/gestalt_graphics/gestalt_graphics.py').read_text():
        raise RuntimeError('Runtime graphics class missing')
    template = (ROOT / 'src/templates/vehicle_with_simple_body_colour_remaps_road.pynml').read_text()
    if 'model_variant.livery_def.livery_name' not in template:
        raise RuntimeError('008d catalogue-driven callback path missing')
    # Keep original class definitions and insert the new ones only once, at EOF.
    existing = ('class PaxLocalTramRuntimeRemapSpike(PaxLocalTram)' in schema_source,
                'class PaxExpressCoachRuntimeRemapSpike(PaxExpressCoach)' in schema_source)
    if existing == (False, False):
        if 'class PaxLocalTram(TrackTypeMixinTram, PaxHaulerLocalConsistBase)' not in schema_source or 'class PaxExpressCoach(TrackTypeMixinTruckBusCoach, PaxHaulerConsistBase)' not in schema_source:
            raise RuntimeError('Parent passenger schema classes changed')
        new_schema = schema_source.rstrip() + SCHEMA_ADDITION + '\n'
    elif existing == (True, True) and schema_source.count('class PaxLocalTramRuntimeRemapSpike(') == 1 and schema_source.count('class PaxExpressCoachRuntimeRemapSpike(') == 1:
        new_schema = schema_source
    else:
        raise RuntimeError('Partial or conflicting schema insertion')
    edits = [(SCHEMAS, schema_source, new_schema)]
    for model, (original, replacement, numeric_id) in TARGETS.items():
        path = VEHICLES / f'{model}.py'
        before = path.read_text()
        edits.append((path, before, update_model(path, original, replacement, numeric_id)))
    # Validate all inputs before writing any output.
    for path, before, after in edits:
        ast.parse(after, filename=str(path))
    for path, before, after in edits:
        if before != after:
            path.write_text(after)
    print('008f: four coaches and five passenger trams; three catalogue liveries each')
    print('CABBAGE352: verify articulated tram units share one random colour selection in-game')


if __name__ == '__main__':
    main()
