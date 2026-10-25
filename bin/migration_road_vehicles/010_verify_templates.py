#!/usr/bin/env python3
"""Stage 010: validate Stage 009 infrastructure and fail closed on incomplete rollout.

PASS for template infrastructure does NOT imply vehicle rendering or Landrace parity.
A full migration requires configured vehicles, actual builds and verified NML parity.
"""
from __future__ import annotations
import argparse
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NAMES = ('vehicle_with_cargo_specific_liveries.pynml','vehicle_with_visible_cargo.pynml')


def check(root):
    model = root / 'src/road_vehicle/model_def.py'
    schemas = root / 'src/road_vehicle/schemas.py'
    templates = root / 'src/templates'
    reasons = []
    for p in (model, schemas):
        if not p.is_file(): reasons.append('missing: '+str(p)); continue
        try: ast.parse(p.read_text(encoding='utf8'))
        except SyntaxError as exc: reasons.append('syntax: '+str(exc))
    if not reasons:
        fields = {n.target.id for n in ast.walk(ast.parse(model.read_text())) if isinstance(n,ast.AnnAssign) and isinstance(n.target,ast.Name)}
        for name in ('graphics_template','cargo_row_map','num_cargo_sprite_variants','generic_rows','cargo_random_switch_expressions'):
            if name not in fields:reasons.append('missing ModelDef field: '+name)
        selector = schemas.read_text()
        if 'template = templates[choice]' not in selector: reasons.append('template dispatch missing')
    for name in NAMES:
        path = templates/name
        if not path.is_file():reasons.append('missing template: '+name);continue
        source = path.read_text(encoding='utf8')
        for forbidden in ('consist.gestalt_graphics','${vehicle.id}','${consist.id}'):
            if forbidden in source:reasons.append(name+' legacy dependency: '+forbidden)
        for required in ('graphics_switches.pynml','capacity_switches.pynml','properties.pynml'):
            if required not in source:reasons.append(name+' missing include: '+required)
    return reasons


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,default=ROOT)
    args=p.parse_args()
    root=args.root.resolve()
    reasons=check(root)
    s8=root/'migration_state/reports/vehicle_stage_008_pass1.json'
    try:
        if json.loads(s8.read_text(encoding='utf8')).get('pass') is not True:
            reasons.append('Stage 008 structural gate did not pass')
    except (OSError,ValueError): reasons.append('Stage 008 baseline absent')
    stage9=root/'migration_state/reports/vehicle_stage_009.json'
    try:
        if json.loads(stage9.read_text(encoding='utf8')).get('pass') is not True:
            reasons.append('Stage 009 install not complete')
    except (OSError,ValueError):reasons.append('Stage 009 report absent')
    report={'stage':10,'scope':'template_infrastructure_validation',
            'pass':not reasons,'checks':{'static_template_contract':not bool(reasons)},
            'issues':reasons, 'template_vehicle_parity_verified':False,
            'landrace_parity_verified':False, 'cutover_approved':False,
            'CABBAGE':'Vehicle opt-in, cargo mappings, rendered builds and parity remain deferred.'}
    dest=root/'migration_state/reports/vehicle_stage_010.json'
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    print('Stage 010 template infrastructure:', 'PASS' if report['pass'] else 'FAIL')
    print('Vehicle graphics parity: NOT VERIFIED; cutover: NOT APPROVED')
    for issue in reasons: print('FAIL:',issue)
    if reasons:raise SystemExit(1)

if __name__=='__main__':main()
