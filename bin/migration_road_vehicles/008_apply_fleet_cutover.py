#!/usr/bin/env python3
"""CABBAGE: Apply the compiled Stage 007 candidate fleet as a reversible Pass 1 cutover.

Not a feature-parity approval. Explicit --apply is required. Roll back with
--rollback using the durable on-disk backup journal; NEVER use a blind git reset
for recovery from a partial application.
"""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write_atomic(path, data):
    temp = path.with_name(path.name + '.stage008_cutover_tmp')
    if temp.exists():
        raise RuntimeError(f'Occupied temporary file: {temp}')
    try:
        with temp.open('xb') as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, path)
    finally:
        if temp.exists():
            temp.unlink()


def load_json(path):
    if not path.is_file():
        raise RuntimeError(f'Missing required evidence: {path}')
    return json.loads(path.read_text(encoding='utf8'))


def inventory(root):
    report = load_json(root / 'migration_state/reports/vehicle_stage_007.json')
    pass1 = load_json(root / 'migration_state/reports/vehicle_stage_008_pass1.json')
    trial = load_json(root / 'migration_state/reports/vehicle_stage_008.json')
    restore = load_json(root / 'migration_state/stage_008_trial/restore_journal.json')
    fresh = load_json(root / 'migration_state/stage_008_trial/outputs/road-hog/freshness_manifest.json')
    if pass1.get('pass') is not True or not all(pass1.get('checks', {}).values()):
        raise RuntimeError('Stage 008 structural acceptance is not PASS')
    if trial.get('candidate_count') != 132 or trial.get('production_vehicle_files_restored') is not True:
        raise RuntimeError('Stage 008 trial does not demonstrate 132 candidates/restoration')
    if trial.get('generated_reference_modified') is not False or restore.get('restored') is not True:
        raise RuntimeError('Golden reference protection or trial restoration not verified')
    builds = {b.get('roster'): b for b in trial.get('builds', [])}
    if set(builds) != {'road-hog', 'heqs'} or any(b.get('returncode') != 0 or b.get('fresh_nml') is not True for b in builds.values()):
        raise RuntimeError('Both Makefile builds must have succeeded with fresh NML')
    if fresh.get('freshness_verified') is not True or fresh.get('roster') != 'road-hog':
        raise RuntimeError('Fresh road-hog outputs not verified')
    data = {}
    for entry in report.get('files', []):
        if entry.get('status') == 'already_model_def':
            continue
        name = entry.get('file')
        if not isinstance(name, str) or Path(name).name != name or name in ('.', '..') or not name.endswith('.py'):
            raise RuntimeError(f'Unsafe candidate filename: {name}')
        src = root / 'src/vehicles' / name
        cand = root / 'migration_state/vehicle_cutover_candidates' / name
        if not src.is_file() or not cand.is_file():
            raise RuntimeError(f'Missing vehicle or candidate: {name}')
        original = src.read_bytes()
        converted = cand.read_bytes()
        if digest(original) != entry.get('source_sha256'):
            raise RuntimeError(f'Stale source since Stage 007: {name}')
        ast.parse(converted, filename=name)
        data[name] = (original, converted)
    if len(data) != 132 or trial['candidate_count'] != len(data):
        raise RuntimeError(f'Expected 132 candidates, found {len(data)}')
    return data


def rollback(root, directory):
    journal_path = directory / 'journal.json'
    journal = load_json(journal_path)
    if journal.get('version') != 1 or not isinstance(journal.get('files'), dict):
        raise RuntimeError('Invalid cutover rollback journal')
    backups = {}
    for name, item in journal['files'].items():
        if Path(name).name != name:
            raise RuntimeError('Unsafe rollback file name')
        backup = directory / 'originals' / name
        if not backup.is_file():
            raise RuntimeError(f'Missing backup {name}')
        content = backup.read_bytes()
        if digest(content) != item['original_sha256']:
            raise RuntimeError(f'Corrupt backup: {name}')
        target = root / 'src/vehicles' / name
        if not target.is_file() or digest(target.read_bytes()) not in (item['original_sha256'], item['candidate_sha256']):
            raise RuntimeError(f'Unrecognised edits to {name}; refusing overwrite')
        backups[name] = content
    for name, content in backups.items():
        target = root / 'src/vehicles' / name
        if target.read_bytes() != content:
            write_atomic(target, content)
    journal['state'] = 'rolled_back'
    journal_path.write_text(json.dumps(journal, indent=2) + '\n', encoding='utf8')
    print(f'ROLLED BACK: {len(backups)} originals restored')


def apply(root, directory):
    if directory.exists():
        raise RuntimeError(f'Cutover journal already exists: {directory}; inspect or --rollback, do not overwrite')
    files = inventory(root)  # validate EVERYTHING before any modifications
    originals = directory / 'originals'
    originals.mkdir(parents=True, exist_ok=False)
    rows = {}
    for name, (original, candidate) in files.items():
        backup = originals / name
        with backup.open('xb') as stream:
            stream.write(original)
            stream.flush()
            os.fsync(stream.fileno())
        rows[name] = {'original_sha256': digest(original), 'candidate_sha256': digest(candidate)}
    journal = directory / 'journal.json'
    journal.write_text(json.dumps({'version': 1, 'state': 'applying', 'scope': 'compile_only_no_feature_parity',
                                  'files': rows}, indent=2) + '\n', encoding='utf8')
    with journal.open('rb') as stream:
        os.fsync(stream.fileno())
    try:
        for name, (original, candidate) in files.items():
            target = root / 'src/vehicles' / name
            if target.read_bytes() != original:
                raise RuntimeError(f'Source changed during cutover: {name}')
            write_atomic(target, candidate)
        for name, (_, candidate) in files.items():
            if (root / 'src/vehicles' / name).read_bytes() != candidate:
                raise RuntimeError(f'Candidate verification failed: {name}')
    except BaseException:
        print('Cutover interrupted/failed: rollback journal retained. Run --rollback before other edits.', file=sys.stderr)
        raise
    journal_data = load_json(journal)
    journal_data['state'] = 'applied'
    journal.write_text(json.dumps(journal_data, indent=2) + '\n', encoding='utf8')
    print('APPLIED: 132 compiled Stage 007 candidates; source remains migrated')
    print('Scope: compile-only; feature parity NOT VERIFIED')
    print('Rollback: python3 bin/migration_road_vehicles/008_apply_fleet_cutover.py --rollback')
    print('Review git diff before committing migrated src/')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--apply', action='store_true')
    action.add_argument('--rollback', action='store_true')
    action.add_argument('--check', action='store_true')
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    directory = root / 'migration_state/stage_008_cutover'
    try:
        if args.rollback:
            rollback(root, directory)
        elif args.check:
            files = inventory(root)
            print(f'READY: {len(files)} compiled candidates; source unchanged')
        else:
            apply(root, directory)
    except (RuntimeError, OSError, SyntaxError, KeyError, TypeError, ValueError) as exc:
        raise SystemExit(f'REFUSED: {exc}') from exc


if __name__ == '__main__':
    main()
