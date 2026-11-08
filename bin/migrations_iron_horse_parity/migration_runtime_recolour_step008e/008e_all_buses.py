#!/usr/bin/env python3
"""008e: Extend three runtime recolour variants to all PaxLocalBus models."""
from pathlib import Path
import ast

ROOT = Path.cwd()
VEHICLES = ROOT / 'src/vehicles'
MODELS = ('highgate_pax', 'thunder_pax', 'topley_pax')
LIVERIES = (
    'RANDOM_LIVERIES_COMPLEMENT_COMPANY_COLOUR',
    'RANDOM_LIVERIES_CLOVER_OCHRE_SULPHUR',
    'RANDOM_LIVERIES_TEAL_PEWTER_SILVER',
)
OLD_SCHEMA = 'schema_name="PaxLocalBus",'
NEW_SCHEMA = 'schema_name="PaxLocalBusRuntimeRemapSpike",'

def updated_source(path, source):
    tree = ast.parse(source, filename=str(path))
    defs = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'ModelDef']
    if len(defs) != 1:
        raise RuntimeError(f'{path}: expected exactly one ModelDef')
    kwargs = {kw.arg: kw.value for kw in defs[0].keywords}
    if 'schema_name' not in kwargs or 'liveries' in kwargs and not isinstance(kwargs['liveries'], ast.List):
        raise RuntimeError(f'{path}: unexpected model structure')
    schema = ast.literal_eval(kwargs['schema_name'])
    if schema not in ('PaxLocalBus', 'PaxLocalBusRuntimeRemapSpike'):
        raise RuntimeError(f'{path}: unexpected schema {schema}')
    if 'liveries' in kwargs:
        current = tuple(ast.literal_eval(kwargs['liveries']))
        if current != LIVERIES:
            raise RuntimeError(f'{path}: conflicting existing liveries {current}')
    else:
        # Insert only at the name line, preserving declaration style and order.
        name = ast.literal_eval(kwargs['name'])
        anchor = f'        name="{name}",'
        if source.count(anchor) != 1:
            raise RuntimeError(f'{path}: name anchor changed')
        added = anchor + '\n' + '        # CABBAGE352 008e: three catalogue-driven runtime recolour variants.\n' + '        liveries=[\n' + ''.join(f'            "{livery}",\n' for livery in LIVERIES) + '        ],'
        source = source.replace(anchor, added)
    if OLD_SCHEMA in source:
        if source.count(OLD_SCHEMA) != 1:
            raise RuntimeError(f'{path}: unexpected schema count')
        source = source.replace(OLD_SCHEMA, NEW_SCHEMA)
    if source.count(NEW_SCHEMA) != 1:
        raise RuntimeError(f'{path}: missing intended graphics schema')
    return source

def main():
    # Verify caller infrastructure and the committed Leyburn test before touching files.
    schema = (ROOT / 'src/road_vehicle/schemas.py').read_text()
    template = (ROOT / 'src/templates/vehicle_with_simple_body_colour_remaps_road.pynml').read_text()
    leyburn = (VEHICLES / 'leyburn_pax.py').read_text()
    if 'class PaxLocalBusRuntimeRemapSpike(PaxLocalBus)' not in schema:
        raise RuntimeError('Missing 008c passenger graphics schema')
    if 'model_variant.livery_def.livery_name' not in template or 'purchase_colour_mapping' not in template:
        # purchase callback is in properties.pynml, not in the graphics template
        if 'model_variant.livery_def.livery_name' not in template or '_purchase_colour_mapping' not in template:
            raise RuntimeError('Missing 008d runtime and purchase recolour switches')
    if 'schema_name="PaxLocalBusRuntimeRemapSpike"' not in leyburn or not all(l in leyburn for l in LIVERIES):
        raise RuntimeError('Missing committed 008d Leyburn baseline')
    pending = []
    for model in MODELS:
        path = VEHICLES / f'{model}.py'
        before = path.read_text()
        after = updated_source(path, before)
        pending.append((path, before, after))
    # All files checked before edits. Staged writes are deterministic and rerunnable.
    for path, before, after in pending:
        if after != before:
            path.write_text(after)
    print('008e: Highgate, Thunder, Topley: CC mix / Pineapple / Ocean Silver (3 each); Leyburn unchanged')

if __name__ == '__main__':
    main()
