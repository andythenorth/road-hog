#!/usr/bin/env python3
"""CABBAGE REVIEW AUDIT: inventory compatibility bridges for a future agent.

This is a review aid, NOT proof every conditional is migration-only. Keep
unreviewed candidates visible instead of inventing justifications.
"""
from __future__ import annotations
import ast
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / 'migration_state/reports/cabbage_bridge_audit.json'
SOURCES = [ROOT / 'src/road_vehicle' / name for name in
           ('model_def.py', 'catalogue.py', 'schemas.py', 'units.py')]
SOURCES += sorted((ROOT / 'bin/migration_road_vehicles').glob('*.py'))
TERMS = ('legacy', 'migration', 'shim', 'compatib', 'fallback', 'deprecated',
         'old ', 'old_', 'road_hog', 'consist', 'unit_def', 'base_platform',
         'sprites_complete', 'power_by_power_source', 'fixed_run_cost_points')


def audit(path):
    source = path.read_text(encoding='utf8')
    lines = source.splitlines()
    tree = ast.parse(source, filename=str(path))
    markers = []
    for index, line in enumerate(lines, 1):
        if 'CABBAGE' in line.upper():
            markers.append({'line': index, 'text': line.strip()[:180]})
    candidates = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.If, ast.IfExp)):
            continue
        text = ast.get_source_segment(source, node.test) or ''
        if not any(term in text.lower() for term in TERMS):
            continue
        line = node.lineno
        preceding = '\n'.join(lines[max(0, line - 5):line])
        # CABBAGE REVIEW REQUIRED means the bridge candidate has no adjacent
        # CABBAGE rationale; do not auto-annotate unknown runtime behaviour.
        candidates.append({'line': line, 'condition': text[:280],
                           'marked_nearby': 'CABBAGE' in preceding.upper(),
                           'review_required': 'CABBAGE' not in preceding.upper()})
    return {'file': str(path.relative_to(ROOT)), 'markers': markers,
            'conditional_candidates': candidates}


def main():
    data = [audit(p) for p in SOURCES if p.is_file()]
    report = {'purpose': 'future agent CABBAGE review; source-only audit',
              'caution': 'Unmarked candidates are not automatically migration shims; decide explicitly.',
              'files': data,
              'marker_count': sum(len(item['markers']) for item in data),
              'review_required_count': sum(sum(x['review_required'] for x in item['conditional_candidates']) for item in data)}
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + '\n', encoding='utf8')
    print(f"CABBAGE markers: {report['marker_count']}; conditional candidates needing review: {report['review_required_count']}")
    print('Report:', REPORT.relative_to(ROOT))

if __name__ == '__main__':
    main()
