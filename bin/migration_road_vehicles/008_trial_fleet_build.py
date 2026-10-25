#!/usr/bin/env python3
"""Run the Stage 007 entire-fleet candidates in an isolated copy of Road Hog.

CABBAGE This deliberately permits incomplete candidates in the COPY so actual
runtime errors can be collected. It never writes to src/vehicles in the checkout.
"""
from __future__ import annotations
import argparse
import ast
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / 'migration_state/reports'
CANDIDATES = ROOT / 'migration_state/vehicle_cutover_candidates'
STAGE7 = REPORT_DIR / 'vehicle_stage_007.json'
TRIAL_DIR = ROOT / 'migration_state/stage_008_trial'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def copy_checkout(destination):
    # Keep graphics, templates, tooling and Makefile as-is. Skip build outputs and
    # VCS metadata; never recurse into the trial destination itself.
    ignored = {'.git', '.venv', 'venv', '__pycache__', '.mypy_cache', '.pytest_cache',
               'migration_state', '.DS_Store'}
    def ignore(_directory, names):
        return [n for n in names if n in ignored or n.endswith('.pyc')]
    shutil.copytree(ROOT, destination, ignore=ignore, symlinks=True)


def run_cmd(command, cwd, logfile):
    with logfile.open('w', encoding='utf8') as out:
        proc = subprocess.run(command, cwd=cwd, stdout=out, stderr=subprocess.STDOUT,
                              text=True, check=False)
    return proc.returncode


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--build', action='store_true', help='run both real roster Makefile builds in the disposable checkout')
    ap.add_argument('--rosters', nargs=2, default=['road-hog', 'heqs'], metavar=('ROSTER1', 'ROSTER2'))
    ap.add_argument('--pw', type=int, default=16)
    ap.add_argument('--retain', action='store_true', help='retain the disposable checkout for debugging')
    args = ap.parse_args()
    if TRIAL_DIR.exists():
        raise SystemExit(f'REFUSED: existing trial directory (remove manually): {TRIAL_DIR}')
    if not STAGE7.exists():
        raise SystemExit('Run Stage 007 first: its report is absent')
    report7 = json.loads(STAGE7.read_text(encoding='utf8'))
    candidates = {}
    stale = []
    for entry in report7['files']:
        name = entry['file']
        if entry.get('status') == 'already_model_def':
            continue
        candidate = CANDIDATES / name
        original = ROOT / 'src/vehicles' / name
        if not candidate.is_file() or not original.is_file():
            stale.append(name + ': missing candidate/source')
            continue
        if sha(original.read_bytes()) != entry.get('source_sha256'):
            stale.append(name + ': source modified since Stage 007')
            continue
        code = candidate.read_text(encoding='utf8')
        try:
            ast.parse(code, filename=name)
        except SyntaxError as exc:
            stale.append(f'{name}: invalid candidate: {exc}')
            continue
        candidates[name] = code
    if stale:
        print('REFUSED: Stage 007 candidates are stale/invalid; re-run Stage 007')
        for item in stale[:25]: print(' ', item)
        raise SystemExit(1)
    if not candidates:
        raise SystemExit('REFUSED: no candidate files')
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    TRIAL_DIR.mkdir(parents=True)
    checkout = TRIAL_DIR / 'checkout'
    try:
        copy_checkout(checkout)
        for name, code in candidates.items():
            target = checkout / 'src/vehicles' / name
            target.write_text(code, encoding='utf8')
        scripts = checkout / 'src/vehicles'
        # Compile all Python modules without invoking their dependencies.
        syntax_errors = []
        for path in scripts.glob('*.py'):
            try: compile(path.read_bytes(), str(path), 'exec')
            except SyntaxError as exc: syntax_errors.append(f'{path.name}: {exc}')
        summary = {
            'stage': 8,
            'mode': 'build' if args.build else 'syntax_only',
            'candidate_files_installed_in_copy': len(candidates),
            'real_checkout_modified': False,
            'syntax_errors': syntax_errors,
            'builds': [],
            'prior_static_issues': report7.get('issues', {}),
            'accepted_for_parity': False,
        }
        if args.build and not syntax_errors:
            if not (checkout / 'Makefile').exists():
                summary['error'] = 'Makefile missing: cannot build snapshot'
            else:
                for roster in args.rosters:
                    cmd = ['make', 'install', f'PW={args.pw}', f'GRF={roster}']
                    log = TRIAL_DIR / f'build_{roster}.log'
                    print('RUN:', ' '.join(cmd), flush=True)
                    rc = run_cmd(cmd, checkout, log)
                    summary['builds'].append({'roster': roster, 'returncode': rc,
                                             'log': str(log.relative_to(ROOT))})
                    print(f'  {roster}: exit {rc}', flush=True)
        result = REPORT_DIR / 'vehicle_stage_008.json'
        result.write_text(json.dumps(summary, indent=2) + '\n', encoding='utf8')
        print('Stage 008: installed', len(candidates), 'candidates ONLY IN disposable copy')
        print('Report:', result.relative_to(ROOT))
        if syntax_errors:
            print('Syntax errors:', *syntax_errors[:15], sep='\n  ')
        if args.build:
            for item in summary['builds']:
                print('Build:', item['roster'], 'status', item['returncode'], 'log', item['log'])
            if not summary['builds'] or any(b['returncode'] for b in summary['builds']):
                raise SystemExit('FAIL: fleet cutover trial build failed; see per-roster logs')
        if syntax_errors: raise SystemExit('FAIL: candidate syntax errors')
        print('PASS: candidate syntax; not a runtime or golden parity claim')
    finally:
        if not args.retain and checkout.exists():
            shutil.rmtree(checkout)


if __name__ == '__main__':
    main()
