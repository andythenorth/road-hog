#!/usr/bin/env python3
"""Provision shared runtime livery names on RH schema base classes. Idempotent."""
from pathlib import Path
import ast

SCHEMAS = Path('src/road_vehicle/schemas.py')
NAMES = (
    'RANDOM_LIVERIES_COMPLEMENT_COMPANY_COLOUR',
    'RANDOM_LIVERIES_CLOVER_OCHRE_SULPHUR',
    'RANDOM_LIVERIES_TEAL_PEWTER_SILVER',
)
CLASSES = (
    'PaxHaulerConsistBase',
    'BoxHaulerConsistBase', 'CoveredHopperHaulerConsistBase',
    'FruitVegHaulerConsistBase', 'LivestockHaulerConsistBase',
    'RefrigeratedHaulerConsistBase', 'TankerConsistBase',
)

def main():
    s = SCHEMAS.read_text()
    tree = ast.parse(s)
    classes = {n.name:n for n in tree.body if isinstance(n, ast.ClassDef)}
    missing = set(CLASSES)-set(classes)
    if missing: raise RuntimeError(f'Missing schema classes: {sorted(missing)}')
    lines = s.splitlines(keepends=True)
    updates = []
    for name in CLASSES:
        cls = classes[name]
        assignments = [n for n in cls.body if isinstance(n, (ast.Assign,ast.AnnAssign)) and any(isinstance(t, ast.Name) and t.id=='liveries' for t in (n.targets if isinstance(n, ast.Assign) else [n.target]))]
        if assignments:
            if len(assignments)!=1 or tuple(ast.literal_eval(assignments[0].value))!=NAMES:
                raise RuntimeError(f'{name}.liveries differs from the planned shared list')
            continue
        content = '    liveries = [\n' + ''.join(f'        "{n}",\n' for n in NAMES) + '    ]\n\n'
        # Immediately after class declaration, before any methods/docstrings.
        updates.append((cls.lineno, content))
    for line_no, content in sorted(updates, reverse=True):
        lines.insert(line_no, content)
    new = ''.join(lines)
    ast.parse(new)
    if new != s: SCHEMAS.write_text(new)
    print(f'010a: {len(updates)} schema classes updated')

if __name__ == '__main__':main()
