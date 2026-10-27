#!/usr/bin/env python3
# 008d: Leyburn catalogue-driven runtime recolour variants.
from pathlib import Path
import ast

ROOT = Path.cwd()
LIVERY = ROOT / 'src/road_vehicle/livery.py'
MODEL = ROOT / 'src/vehicles/leyburn_pax.py'
GRAPHICS = ROOT / 'src/templates/vehicle_with_simple_body_colour_remaps_road.pynml'
CONSTANTS = ROOT / 'src/global_constants.py'
NAMES = (
    'RANDOM_LIVERIES_COMPLEMENT_COMPANY_COLOUR',
    'RANDOM_LIVERIES_CLOVER_OCHRE_SULPHUR',
    'RANDOM_LIVERIES_TEAL_PEWTER_SILVER',
)

def replace_once(path, before, after):
    source = path.read_text()
    if after in source:
        return False
    if source.count(before) != 1:
        raise RuntimeError(f'{path}: expected one anchor, found {source.count(before)}')
    path.write_text(source.replace(before, after))
    return True

def main():
    for path in (LIVERY, MODEL, GRAPHICS, CONSTANTS):
        if not path.is_file():
            raise RuntimeError(f'Missing prerequisite: {path}')
    tree = ast.parse(CONSTANTS.read_text())
    definitions = [node.value for node in tree.body if isinstance(node, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == 'freight_wagon_liveries' for t in node.targets)]
    if len(definitions) != 1 or not isinstance(definitions[0], ast.Dict):
        raise RuntimeError('Missing freight_wagon_liveries dictionary')
    keys = [k.value for k in definitions[0].keys if isinstance(k, ast.Constant)]
    for name in NAMES:
        if name not in keys:
            raise RuntimeError(f'Missing IH recolour livery: {name}')
    if len(set(keys)) != len(keys):
        # Existing IH duplicate key is unrelated, but warn explicitly: index follows first occurrence.
        print('CABBAGE352: duplicate keys in freight_wagon_liveries; dictionary index uses first occurrence')

    # No additional graphics rows: all three catalogue entries share the existing spritesheet.
    livery_anchor = 'livery_supplier.add_livery("DEFAULT")'
    livery_added = '''livery_supplier.add_livery("DEFAULT")
# CABBAGE352 008d: register the three runtime-remap catalogue liveries.
for _name in (
    "RANDOM_LIVERIES_COMPLEMENT_COMPANY_COLOUR",
    "RANDOM_LIVERIES_CLOVER_OCHRE_SULPHUR",
    "RANDOM_LIVERIES_TEAL_PEWTER_SILVER",
):
    livery_supplier.add_livery(
        _name,
        is_freight_wagon_livery=True,
        **global_constants.freight_wagon_liveries[_name],
    )'''
    model_anchor = '        name="Leyburn",'
    model_added = '''        name="Leyburn",
        # CABBAGE352 008d: catalogue entries in purchase order; reserve numeric IDs 20..22.
        liveries=[
            "RANDOM_LIVERIES_COMPLEMENT_COMPANY_COLOUR",
            "RANDOM_LIVERIES_CLOVER_OCHRE_SULPHUR",
            "RANDOM_LIVERIES_TEAL_PEWTER_SILVER",
        ],'''
    gfx_old = '''<!--! CABBAGE352: initial single-vehicle Pineapple test caller.
      The 008b badge lookup remains disabled; catalogue-driven livery selection follows in 009.
      24 is the random-choice temporary register used by the IH procedure port. -->
switch (FEAT_ROADVEHS, SELF, ${unit.id}_runtime_colour_mapping,
    [STORE_TEMP(random_bits_wagon_random_remap_livery(), 24),
     switch_freight_wagon_livery_serialised_liveries(12)]) {
    return;
}

switch (FEAT_ROADVEHS, SELF, ${unit.id}_purchase_colour_mapping,
    [STORE_TEMP(0, 24),
     switch_freight_wagon_livery_serialised_liveries(36)]) {
    return;
}'''
    gfx_new = '''<!--! CABBAGE352 008d: resolve runtime mapping from catalogue livery; IH dictionary order
      must match the serialised lookup table rendered in the NML header. -->
switch (FEAT_ROADVEHS, SELF, ${unit.id}_runtime_colour_mapping,
    [STORE_TEMP(random_bits_wagon_random_remap_livery(), 24),
     switch_freight_wagon_livery_serialised_liveries(${list(global_constants.freight_wagon_liveries).index(model_variant.livery_def.livery_name)})]) {
    return;
}

switch (FEAT_ROADVEHS, SELF, ${unit.id}_purchase_colour_mapping,
    [STORE_TEMP(0, 24),
     switch_freight_wagon_livery_serialised_liveries(${len(global_constants.freight_wagon_liveries) + list(global_constants.freight_wagon_liveries).index(model_variant.livery_def.livery_name)})]) {
    return;
}'''
    # Check ALL inputs before any edits.
    operations = ((LIVERY, livery_anchor, livery_added),
                  (MODEL, model_anchor, model_added),
                  (GRAPHICS, gfx_old, gfx_new))
    for path, old, new in operations:
        value = path.read_text()
        if new not in value and value.count(old) != 1:
            raise RuntimeError(f'{path}: expected exactly one known 008c anchor; no files changed')
    for path, old, new in operations:
        replace_once(path, old, new)
    print('008d: Leyburn catalogue liveries connected (CC mix, Pineapple, Ocean Silver), IDs 20..22')

if __name__ == '__main__':
    main()
