#!/usr/bin/env python3
"""Verify existing Road Hog clone support before catalogue variant migration.

Run from the Road Hog repository root.
"""
from pathlib import Path
import ast

path = Path('src/road_vehicle/model_def.py')
source = path.read_text()
module = ast.parse(source, filename=str(path))
cloner = next((n for n in module.body if isinstance(n, ast.ClassDef) and n.name == 'ModelDefCloner'), None)
if cloner is None:
    raise SystemExit('Missing ModelDefCloner')
methods = {n.name for n in cloner.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
assert {'begin_clone', 'complete_clone'} <= methods, 'Missing clone lifecycle method'
checks = {
    'source clone reference': 'cloned_from_model_def = model_def',
    'source clone bookkeeping': 'model_def.clones.append(cloned_model_def)',
    'independent numeric ID': 'cloned_model_def.base_numeric_id = base_numeric_id',
    'generated clone ID': 'model_def.model_id + "_clone_"',
    'source vehicle family': 'cloned_model_def.vehicle_family_id = model_def.model_id',
    'unit repeats': 'unit_def.repeat = unit_repeats[counter]',
    'Road Hog power adjustment': 'model_def.power * model_def.clone_stats_adjustment_factor',
}
for label, fragment in checks.items():
    if fragment not in source:
        raise SystemExit(f'Clone support check failed: {label}')
print('Step 004: existing Road Hog clone support verified; no source changes required.')
