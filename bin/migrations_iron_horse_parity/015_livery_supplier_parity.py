#!/usr/bin/env python3
"""Migration 015: use one compile-scoped LiverySupplier, as in Iron Horse.

Run from the Road Hog repository root.  Refuses unexpected source layouts.
Does not modify vehicle declarations, catalogue allocation, or badge behaviour.
"""
from pathlib import Path
import ast

ROOT = Path('src')


def replace_once(text, old, new, path):
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'{path}: expected exactly one occurrence, found {count}: {old[:75]!r}')
    return text.replace(old, new, 1)


def main():
    paths = {
        'road_hog': ROOT / 'road_hog.py',
        'livery': ROOT / 'road_vehicle/livery.py',
        'catalogue': ROOT / 'road_vehicle/catalogue.py',
        'render_nml': ROOT / 'render_nml.py',
    }
    before = {key: path.read_text() for key, path in paths.items()}
    after = dict(before)

    p = paths['road_hog']
    s = after['road_hog']
    s = replace_once(s, 'from badges.badge import BadgeManager\n',
        'from badges.badge import BadgeManager\nfrom road_vehicle.livery import LiverySupplier\n', p)
    s = replace_once(s,
        '    globals()["badge_manager"] = BadgeManager()\n',
        '    globals()["livery_supplier"] = LiverySupplier()\n'
        '    globals()["badge_manager"] = BadgeManager()\n', p)
    s = replace_once(s,
        '    # rosters\n    roster_manager.add_rosters(',
        '    # liveries\n'
        '    livery_supplier.add_livery("DEFAULT")\n'
        '    for livery_name, livery_def in global_constants.freight_wagon_liveries.items():\n'
        '        livery_supplier.add_livery(\n'
        '            livery_name, is_freight_wagon_livery=True, **livery_def\n'
        '        )\n\n'
        '    # rosters\n    roster_manager.add_rosters(', p)
    after['road_hog'] = s

    p = paths['livery']
    s = after['livery']
    old = '''# Road Hog default, retained for existing vehicle declarations.
livery_supplier = LiverySupplier()
livery_supplier.add_livery("DEFAULT")
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
    )
'''
    s = replace_once(s, old, '', p)
    after['livery'] = s

    p = paths['catalogue']
    s = after['catalogue']
    s = replace_once(s,
        'from .livery import LiveryDef, livery_supplier\n',
        'from .livery import LiveryDef\nimport road_hog\n', p)
    if s.count('livery_supplier.deliver(') != 4:
        raise RuntimeError(f'{p}: expected four livery delivery sites')
    s = s.replace('livery_supplier.deliver(', 'road_hog.livery_supplier.deliver(')
    after['catalogue'] = s

    p = paths['render_nml']
    s = after['render_nml']
    old = '''def runtime_recolour_livery_supplier():
    # CABBAGE352: keep IH livery ordering/serialization for uncalled switches.
    from road_vehicle.livery import LiverySupplier

    supplier = LiverySupplier()
    for name, spec in global_constants.freight_wagon_liveries.items():
        supplier.add_livery(name, is_freight_wagon_livery=True, **spec)
    return supplier


'''
    s = replace_once(s, old, '', p)
    s = replace_once(s,
        'livery_supplier=runtime_recolour_livery_supplier(),',
        'livery_supplier=road_hog.livery_supplier,', p)
    after['render_nml'] = s

    # Validate every prospective edit before writing any file.
    for key, text in after.items():
        ast.parse(text, filename=str(paths[key]))
    for key in paths:
        if after[key] != before[key]:
            paths[key].write_text(after[key])
            print(f'Updated {paths[key]}')
    print('Migration 015 complete')


if __name__ == '__main__':
    main()
