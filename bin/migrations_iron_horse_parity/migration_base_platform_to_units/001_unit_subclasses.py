"""Create unit subclasses from the existing platform declarations."""

import ast
from pathlib import Path

ROOT = Path('src')
UNITS = ROOT / 'road_vehicle/units.py'
PLATFORM_DIR = ROOT / 'base_platforms'
MARK = '# CABBAGE: generated concrete unit subclasses from former BasePlatform data'
FIELDS = ('always_use_same_spriterow', 'capacity', 'cargo_length', 'chassis', 'effects', 'semi_truck_shift_offset_jank', 'unit_is_semi_tractor', 'vehicle_length')


def main():
    text = UNITS.read_text()
    if MARK in text:
        print('Step 001 already applied')
        return
    classes = {}
    for filename in ('trucks.py', 'feldbahn.py', 'trams.py', 'heqs.py'):
        tree = ast.parse((PLATFORM_DIR / filename).read_text())
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                attrs = {}
                for statement in node.body:
                    if isinstance(statement, ast.Assign) and len(statement.targets) == 1 and isinstance(statement.targets[0], ast.Name):
                        attrs[statement.targets[0].id] = statement.value
                parents = [base.id for base in node.bases if isinstance(base, ast.Name)]
                classes[node.name] = (parents, attrs)
    written = []
    for name, (parents, attrs) in classes.items():
        if name.endswith('Base'):
            continue
        combined = {}
        for parent in parents:
            if parent in classes:
                combined.update(classes[parent][1])
        combined.update(attrs)
        typename = ast.unparse(combined.get('type', ast.Name(id='RoadVehicleUnit', ctx=ast.Load())))
        if typename not in ('RoadVehicleUnit', 'DieselVehicleUnit', 'SteamVehicleUnit', 'ElectricVehicleUnit'):
            raise ValueError(f'Unexpected traction class: {name}, {typename}')
        values = {k: ast.unparse(v) for k, v in combined.items() if k in FIELDS}
        block = [f'class {name}({typename}):']
        if values:
            block += ['    def __init__(self, model_variant, unit_def, id, numeric_id):', '        # Former platform values intentionally override UnitDef declarations.', '        from dataclasses import replace', '        unit_def = replace(', '            unit_def,']
            block += [f'            {k}={v},' for k, v in values.items()]
            block += ['        )', '        super().__init__(model_variant, unit_def, id, numeric_id)']
        else:
            block.append('    pass')
        if name == 'WagonFeldbahnA':
            block += ['', '    def get_spritesheet_name_body_or_complete_vehicle(self):', '        return self.model_variant.name_suffix_consist_type.lower() + "_wagon_feldbahn_gen_1"']
        elif 'SemiTractorTruck' in name or 'EngineFeldbahn' in name:
            cname = name
            parts = ''.join(('_'+c.lower()) if c.isupper() else c for c in cname[:-2]).lstrip('_') + '_' + cname[-2:]
            block += ['', '    def get_spritesheet_name_body_or_complete_vehicle(self):', f'        return {parts!r}']
        written.append('\n'.join(block))
    new = text + '\n\n' + MARK + '\n\n' + '\n\n\n'.join(written) + '\n'
    ast.parse(new)
    UNITS.write_text(new)
    print(f'Step 001: added {len(written)} concrete subclasses')


if __name__ == '__main__':
    main()
