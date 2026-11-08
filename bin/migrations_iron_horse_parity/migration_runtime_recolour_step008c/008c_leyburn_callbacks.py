#!/usr/bin/env python3
'Step 008c: one explicitly selected passenger-vehicle runtime recolour caller.'
from pathlib import Path
import ast
import sys

ROOT = Path.cwd()
SCHEMAS = ROOT / 'src/road_vehicle/schemas.py'
VEHICLE = ROOT / 'src/vehicles/leyburn_pax.py'
PROPS = ROOT / 'src/templates/properties.pynml'
GRAPHICS = ROOT / 'src/templates/vehicle_with_simple_body_colour_remaps_road.pynml'
CONSTANTS = ROOT / 'src/global_constants.py'
PROCEDURES = ROOT / 'src/templates/procedures_wagon_recolour_strategies_road.pynml'


def replace_once(path, old, new):
    content = path.read_text()
    if new in content:
        return False
    if content.count(old) != 1:
        raise RuntimeError(f'{path}: expected one replacement anchor, found {content.count(old)}')
    path.write_text(content.replace(old, new))
    return True


def main():
    for path in [SCHEMAS, VEHICLE, PROPS, GRAPHICS, CONSTANTS, PROCEDURES]:
        if not path.is_file():
            raise RuntimeError(f'Missing prerequisite {path}')
    ptext = PROCEDURES.read_text()
    for name in ('switch_freight_wagon_livery_serialised_liveries',
                 'switch_freight_wagon_livery_set_params',
                 'switch_freight_wagon_livery_select_colour_set'):
        if name not in ptext:
            raise RuntimeError(f'Missing step 008b switch {name}')
    if 'k_addr_wagon_recolour_livery_num_' in ptext:
        raise RuntimeError('Apply the 008b register correction first')

    # Read only the literal dict from the checked-in Python file; no imports needed.
    tree = ast.parse(CONSTANTS.read_text())
    definitions = [node.value for node in tree.body if isinstance(node, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == 'freight_wagon_liveries' for t in node.targets)]
    if len(definitions) != 1 or not isinstance(definitions[0], ast.Dict):
        raise RuntimeError('Cannot locate freight_wagon_liveries dictionary')
    names = [key.value for key in definitions[0].keys if isinstance(key, ast.Constant)]
    # Dictionary duplicate keys are replaced without altering insertion position.
    names = list(dict.fromkeys(names))
    index = names.index('RANDOM_LIVERIES_CLOVER_OCHRE_SULPHUR')
    count = len(names)

    schema_anchor = 'class PaxLocalTram(TrackTypeMixinTram, PaxHaulerLocalConsistBase):'
    schema_insert = '''class PaxLocalBusRuntimeRemapSpike(PaxLocalBus):
    # CABBAGE352: one-vehicle callback spike; keep normal PaxLocalBus unchanged.
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.gestalt_graphics = GestaltGraphicsSimpleBodyColourRemaps()


''' + schema_anchor
    replace_once(SCHEMAS, 'from gestalt_graphics.gestalt_graphics import GestaltGraphics',
                 'from gestalt_graphics.gestalt_graphics import GestaltGraphics, GestaltGraphicsSimpleBodyColourRemaps')
    replace_once(SCHEMAS, schema_anchor, schema_insert)
    replace_once(VEHICLE, 'schema_name="PaxLocalBus",', 'schema_name="PaxLocalBusRuntimeRemapSpike",')

    # Pass a known livery dictionary index into the existing IH serialised-params lookup.
    # Store random choice in the same temporary address as the 008b procedure.
    # Purchase choice 0 plus purchase-block offset is deterministic.
    anchor = '''switch (FEAT_ROADVEHS, SELF, ${unit.id}_switch_graphics, 0) {
    return ${unit.id}_sg;
}
'''
    replacement = anchor + f'''
<!--! CABBAGE352: initial single-vehicle Pineapple test caller.
      The 008b badge lookup remains disabled; catalogue-driven livery selection follows in 009.
      24 is the random-choice temporary register used by the IH procedure port. -->
switch (FEAT_ROADVEHS, SELF, ${{unit.id}}_runtime_colour_mapping,
    [STORE_TEMP(random_bits_wagon_random_remap_livery(), 24),
     switch_freight_wagon_livery_serialised_liveries({index})]) {{
    return;
}}

switch (FEAT_ROADVEHS, SELF, ${{unit.id}}_purchase_colour_mapping,
    [STORE_TEMP(0, 24),
     switch_freight_wagon_livery_serialised_liveries({count + index})]) {{
    return;
}}
'''
    replace_once(GRAPHICS, anchor, replacement)
    replace_once(PROPS,
        '''            colour_mapping:                 PALETTE_USE_DEFAULT;
            purchase_colour_mapping:        PALETTE_USE_DEFAULT;''',
        '''            colour_mapping:                 ${unit.id}_runtime_colour_mapping;
            purchase_colour_mapping:        ${unit.id}_purchase_colour_mapping;''')
    print(f'008c: Leyburn callbacks connected; Pineapple livery index {index}, purchase index {count + index}')

if __name__ == '__main__':
    main()
