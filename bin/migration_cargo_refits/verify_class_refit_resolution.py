#!/usr/bin/env python3
"""Verify migration 002 class resolution and template call sites."""
import argparse
import ast
from pathlib import Path
import sys

ALLOWED = 'refittable_cargo_classes:       ${unit.get_cargo_classes_as_nml_prop("allowed")};'
DISALLOWED = 'non_refittable_cargo_classes:   ${unit.get_cargo_classes_as_nml_prop("disallowed")};'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path('.'))
    args = parser.parse_args()
    units = (args.root/'src/road_vehicle/units.py').read_text()
    schemas = (args.root/'src/road_vehicle/schemas.py').read_text()
    template = (args.root/'src/templates/properties.pynml').read_text()
    tree = ast.parse(units)
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'RoadVehicleUnit')
    methods = [n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == 'get_cargo_classes_as_nml_prop']
    assert len(methods) == 1, 'Expected exactly one unit class resolution method'
    method = methods[0]
    assert [arg.arg for arg in method.args.args] == ['self', 'allow_disallow_key']
    # Verify behavior using the actual method against fake Polar Fox data.
    namespace = {'global_constants': type('Constants', (), {'base_refits_by_class': {
        'one': {'allowed': ['CC_PASSENGERS'], 'disallowed': ['CC_MAIL']},
        'two': {'allowed': ['CC_EXPRESS'], 'disallowed': ['CC_BULK']},
    }})()}
    exec(compile(ast.Module(body=[method], type_ignores=[]), '<unit method>', 'exec'), namespace)
    fake = type('Unit', (), {'model_variant': type('Model', (), {'class_refit_groups': ['one','two']})()})()
    assert namespace[method.name](fake, 'allowed') == 'bitmask(CC_PASSENGERS,CC_EXPRESS)'
    assert namespace[method.name](fake, 'disallowed') == 'bitmask(CC_MAIL,CC_BULK)'
    assert template.count(ALLOWED) == 1 and template.count(DISALLOWED) == 1
    assert 'model_variant.refittable_classes' not in template
    assert 'def refittable_classes(self):' not in schemas
    print('PASS: Iron Horse-style allowed/disallowed resolution, both template call sites, obsolete schema property removed.')

if __name__ == '__main__':
    try: main()
    except (AssertionError, OSError, SyntaxError, StopIteration) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        sys.exit(1)
