#!/usr/bin/env python3
"""Standalone Road Hog vehicle NML template pass.

Run from the repository root:
    python3 bin/migration_vehicle_nml_templates/001_vehicle_nml_templates.py

Only modifies src/road_vehicle/schemas.py and the two cargo-specific vehicle
NML templates. No prior migration stage or migration script is required.
"""
from pathlib import Path
import argparse
import difflib
import sys


def replace_once(text, before, after, filename):
    if before not in text:
        if after in text:
            return text
        raise RuntimeError(f"{filename}: expected source fragment not found")
    if text.count(before) != 1:
        raise RuntimeError(f"{filename}: expected a single source fragment")
    return text.replace(before, after, 1)


def updated_files(root):
    schema = root / 'src/road_vehicle/schemas.py'
    old = schema.read_text()
    before = '''            # CABBAGE PASS 1 TEMPLATE SHIM: temporarily force vehicle_default.pynml.
            # CABBAGE FUTURE PASS: restore self.gestalt_graphics.nml_template selection;
            # cargo-specific liveries and visible-cargo rendering remain deferred.
            template = templates["vehicle_default.pynml"]'''
    after = '''            # Vehicle NML template selection belongs to GestaltGraphics.
            template = templates[self.gestalt_graphics.nml_template]'''
    yield schema, old, replace_once(old, before, after, schema)

    for name in ('vehicle_with_visible_cargo.pynml', 'vehicle_with_cargo_specific_liveries.pynml'):
        path = root / 'src/templates' / name
        old = path.read_text()
        new = old.replace('${vehicle.id}', '${unit.id}')
        new = new.replace('${vehicle.spriterow_num', '${unit.spriterow_num')
        new = new.replace('${consist.id}', '${model_variant.model_def.model_id}')
        new = new.replace('consist.gestalt_graphics', 'model_variant.gestalt_graphics')
        new = new.replace('${vehicle.get_nml_expression_for_cargo_variant_random_switch(mapping[0])}', 'SELF, ${unit.id}_switch_graphics_${mapping[0]}, bitmask(TRIGGER_VEHICLE_ANY_LOAD)')
        new = new.replace("${vehicle.get_nml_expression_for_cargo_variant_random_switch('generic_cargos')}", 'SELF, ${unit.id}_switch_graphics_generic_cargos, bitmask(TRIGGER_VEHICLE_ANY_LOAD)')
        if name == 'vehicle_with_visible_cargo.pynml':
            new = new.replace(
                '${vehicle.get_nml_expression_for_cargo_variant_random_switch(mapping[0])}',
                'SELF, ${unit.id}_switch_graphics_${mapping[0]}, bitmask(TRIGGER_VEHICLE_ANY_LOAD)',
            )
            new = new.replace(
                "${vehicle.get_nml_expression_for_cargo_variant_random_switch('generic_cargos')}",
                'SELF, ${unit.id}_switch_graphics_generic_cargos, bitmask(TRIGGER_VEHICLE_ANY_LOAD)',
            )
        if '${vehicle.' in new or 'consist.' in new:
            raise RuntimeError(f'{path}: unmigrated vehicle/consist references')
        yield path, old, new


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, default=Path.cwd())
    ap.add_argument('--check', action='store_true', help='Check files already have the changes; do not write')
    ap.add_argument('--diff', action='store_true', help='Show changes without writing')
    args = ap.parse_args()
    changes = list(updated_files(args.root.resolve()))
    if args.check:
        if any(old != new for _, old, new in changes):
            sys.exit('PASS NOT APPLIED: run without --check')
        print('PASS APPLIED: vehicle NML template dispatch and cargo template interfaces')
        return
    if args.diff:
        for path, old, new in changes:
            sys.stdout.writelines(difflib.unified_diff(old.splitlines(True), new.splitlines(True), fromfile=str(path), tofile=str(path)))
        return
    for path, old, new in changes:
        if old != new:
            path.write_text(new)
            print(f'Updated {path.relative_to(args.root.resolve())}')
        else:
            print(f'Unchanged {path.relative_to(args.root.resolve())}')
    print('Run the full Makefile, then inspect generated/nml/*.nml by vehicle GestaltGraphics.nml_template.')


if __name__ == '__main__':
    main()
