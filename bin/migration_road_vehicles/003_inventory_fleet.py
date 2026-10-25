#!/usr/bin/env python3
"""List the legacy files and unit declarations. We need this for batch conversion."""
from pathlib import Path
import ast
import json
ROOT = Path(__file__).resolve().parents[2]
vehicles = ROOT/'src/vehicles'
report = []
for path in sorted(vehicles.glob('*.py')):
    if path.name == '__init__.py':
        continue
    source = path.read_text(encoding='utf-8')
    tree = ast.parse(source, filename=str(path))
    units = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in ('add_unit', 'add_unit_def'):
            units.append({'line':node.lineno, 'platform': next((ast.unparse(kw.value) for kw in node.keywords if kw.arg=='base_platform'), None), 'repeat':next((ast.unparse(kw.value) for kw in node.keywords if kw.arg=='repeat'), '1')})
    report.append({'file':path.name,'units':units, 'definition_kind':'model' if 'ModelDef(' in source else 'legacy'})
dest=ROOT/'migration_state/reports/vehicle_inventory.json'
dest.parent.mkdir(parents=True,exist_ok=True)
dest.write_text(json.dumps(report,indent=2)+'\n')
print('PASS: wrote',dest.relative_to(ROOT))
print('Vehicle modules:',len(report),'legacy:',sum(x['definition_kind']=='legacy' for x in report))
print('Platform unit declarations:',sum(u['platform'] not in (None,'None') for x in report for u in x['units']))
print('CABBAGE: vehicle files have NOT been converted; the inventory is for reviewed batches.')
