#!/usr/bin/env python3
"""CABBAGE: Stage 008 guarded in-place fleet trial with crash-recoverable backup.

Temporarily installs Stage 007 candidate declarations into the ORIGINAL checkout,
runs its ORIGINAL Makefile and compiler, captures logs, and restores the exact
original vehicle bytes. generated/ is disposable; generated.reference/ is read-only.
This tool intentionally does NOT perform production cutover or certify parity.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "migration_state/reports"
CANDIDATES = ROOT / "migration_state/vehicle_cutover_candidates"
STAGE7 = REPORT_DIR / "vehicle_stage_007.json"
TRIAL_DIR = ROOT / "migration_state/stage_008_trial"
VEHICLES = ROOT / "src/vehicles"
JOURNAL = TRIAL_DIR / "restore_journal.json"
BACKUP = TRIAL_DIR / "original_vehicles"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def atomic_write(path, data):
    tmp = path.with_name(path.name + '.stage008_tmp')
    if tmp.exists():
        raise RuntimeError(f'Refusing occupied temporary path: {tmp}')
    try:
        with tmp.open('xb') as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()


def restore_originals():
    """Restore only candidates that Stage 008 backed up; tolerate partial install."""
    if not JOURNAL.is_file():
        raise RuntimeError('REFUSED: restore journal missing; originals may be modified')
    journal = json.loads(JOURNAL.read_text(encoding='utf8'))
    if journal.get('version') != 1 or not isinstance(journal.get('files'), dict):
        raise RuntimeError('REFUSED: invalid restore journal')
    original_map = {}
    for name, expected in journal['files'].items():
        if Path(name).name != name or name in ('.', '..'):
            raise RuntimeError('REFUSED: invalid journal filename')
        backup = BACKUP / name
        if not backup.is_file():
            raise RuntimeError(f'REFUSED: missing backup for {name}')
        data = backup.read_bytes()
        if sha(data) != expected:
            raise RuntimeError(f'REFUSED: corrupted original backup for {name}')
        original_map[name] = data
    for name, data in original_map.items():
        dest = VEHICLES / name
        if not dest.is_file():
            raise RuntimeError(f'REFUSED: original destination missing: {dest}')
        if dest.read_bytes() != data:
            atomic_write(dest, data)
    for name, data in original_map.items():
        if (VEHICLES / name).read_bytes() != data:
            raise RuntimeError(f'REFUSED: restoration verification failed: {name}')
    journal['restored'] = True
    JOURNAL.write_text(json.dumps(journal, indent=2) + '\n', encoding='utf8')
    print(f'RESTORED: {len(original_map)} production vehicle files byte-for-byte', flush=True)


def prepare_candidates():
    if not STAGE7.is_file():
        raise RuntimeError('Run Stage 007 first: report is absent')
    report7 = json.loads(STAGE7.read_text(encoding='utf8'))
    candidates = {}
    stale = []
    for entry in report7['files']:
        name = entry['file']
        if entry.get('status') == 'already_model_def':
            continue
        if Path(name).name != name or name in ('.', '..'):
            stale.append(f'{name}: unsafe filename')
            continue
        candidate = CANDIDATES / name
        original = VEHICLES / name
        if not candidate.is_file() or not original.is_file():
            stale.append(f'{name}: missing candidate/source')
            continue
        original_data = original.read_bytes()
        if sha(original_data) != entry.get('source_sha256'):
            stale.append(f'{name}: source modified since Stage 007')
            continue
        data = candidate.read_bytes()
        try:
            ast.parse(data, filename=name)
        except SyntaxError as exc:
            stale.append(f'{name}: invalid candidate: {exc}')
            continue
        candidates[name] = (original_data, data)
    if stale:
        raise RuntimeError('REFUSED: stale/invalid Stage 007 candidates:\n  ' + '\n  '.join(stale[:25]))
    if not candidates:
        raise RuntimeError('REFUSED: no candidate files')
    return candidates, report7


def prepare_backups(candidates):
    # CABBAGE Crash-recovery journal is durable before ANY production vehicle edits.
    TRIAL_DIR.mkdir(parents=True, exist_ok=False)
    BACKUP.mkdir()
    original_hashes = {}
    for name, (original, _) in candidates.items():
        dest = BACKUP / name
        with dest.open('xb') as f:
            f.write(original)
            f.flush()
            os.fsync(f.fileno())
        original_hashes[name] = sha(original)
    JOURNAL.write_text(json.dumps({
        'version': 1, 'files': original_hashes, 'restored': False,
        'instruction': 'If interrupted, run this script with --restore before making other edits.'
    }, indent=2) + '\n', encoding='utf8')
    with JOURNAL.open('rb') as f:
        os.fsync(f.fileno())
    return original_hashes


def run_cmd(command, logfile):
    with logfile.open('w', encoding='utf8') as out:
        return subprocess.run(command, cwd=ROOT, stdout=out,
                              stderr=subprocess.STDOUT, check=False).returncode


def snapshot_outputs(roster, build_start_ns):
    """CABBAGE: capture fresh outputs before the next roster overwrites generated/."""
    dest = TRIAL_DIR / 'outputs' / roster
    dest.mkdir(parents=True, exist_ok=True)
    include = []
    for filename in (f'{roster}.nml', f'{roster}.nfo', f'{roster}.grf'):
        include.append(ROOT / 'generated' / filename)
    if roster == 'road-hog':
        for directory, suffix in (('nml', '.nml'), ('graphics', '.png'),
                                  ('lang/road-hog', '.lng')):
            src_dir = ROOT / 'generated' / directory
            if src_dir.is_dir():
                include.extend(p for p in src_dir.rglob('*') if p.is_file() and p.suffix == suffix)
    stale = []
    copied = []
    copied_roadtype_assets = []
    for src in include:
        if not src.exists():
            continue
        if src.is_symlink() or not src.is_file():
            raise RuntimeError(f'REFUSED: non-regular generated output: {src}')
        relative = src.relative_to(ROOT / 'generated')
        # CABBAGE MIGRATION VERIFICATION: roadtype PNGs are copied source
        # assets, not regenerated sprites. Their preserved timestamps are not
        # evidence of stale vehicle output. Retain these files in the snapshot
        # so strict Landrace pixel parity still verifies their actual content.
        # Remove this exception only if roadtype images become generated assets.
        copied_roadtype_asset = (
            roster == 'road-hog'
            and len(relative.parts) >= 4
            and relative.parts[:3] == ('graphics', 'road-hog', 'roadtypes')
            and src.suffix == '.png'
        )
        # CABBAGE MIGRATION VERIFICATION: do not accept stale NML or generated
        # vehicle PNGs from an earlier build; copied roadtype assets excepted.
        if not copied_roadtype_asset and src.stat().st_mtime_ns < build_start_ns:
            stale.append(str(src.relative_to(ROOT)))
            continue
        destination = dest / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, destination)
        copied.append(relative.as_posix())
        if copied_roadtype_asset:
            copied_roadtype_assets.append(relative.as_posix())
    freshness = {'roster': roster, 'build_start_ns': build_start_ns,
                 'freshness_verified': not stale and bool(copied),
                 'stale_files': stale, 'captured_files': copied,
                 'copied_roadtype_assets': copied_roadtype_assets}
    if stale:
        print(f'CABBAGE: {roster} has {len(stale)} stale output files; '
              f'first examples: {stale[:5]}', flush=True)
    (dest / 'freshness_manifest.json').write_text(json.dumps(freshness, indent=2) + '\n', encoding='utf8')
    return dest


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--build', action='store_true', help='run the original Makefile with temporarily converted vehicles')
    ap.add_argument('--rosters', nargs=2, default=['road-hog','heqs'], metavar=('ROSTER1','ROSTER2'))
    ap.add_argument('--pw', type=int, default=16)
    ap.add_argument('--retain', action='store_true', help='keep logs and backup snapshot; vehicle restoration is always mandatory')
    ap.add_argument('--restore', action='store_true', help='recover originals from an interrupted earlier trial')
    args = ap.parse_args()
    if args.restore:
        restore_originals()
        return
    if not args.build:
        raise SystemExit('REFUSED: Stage 008 acceptance requires --build; dry installation is not a PASS')
    if set(args.rosters) != {'road-hog', 'heqs'}:
        raise SystemExit('REFUSED: Stage 008 acceptance requires road-hog and heqs builds')
    if TRIAL_DIR.exists():
        raise SystemExit(f'REFUSED: existing trial directory: {TRIAL_DIR}. '
                         'Use --restore if interrupted; otherwise remove it manually after verifying restoration.')
    if not (ROOT / 'Makefile').is_file():
        raise SystemExit('REFUSED: original Makefile not found')
    candidates, report7 = prepare_candidates()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    prepare_backups(candidates)
    # CABBAGE: the golden reference must remain byte-identical throughout both builds.
    reference_dir = ROOT / 'generated.reference'
    if not reference_dir.is_dir():
        raise SystemExit('REFUSED: missing generated.reference/')
    reference_before_trial = {p.relative_to(reference_dir).as_posix(): sha(p.read_bytes())
                              for p in reference_dir.rglob('*') if p.is_file()}
    summary = {
        'stage': 8, 'mode': 'in_place_trial',
        'candidate_count': len(candidates), 'production_vehicle_files_restored': False,
        'generated_reference_modified': False, 'accepted_for_parity': False,
        'builds': [], 'prior_static_issues': report7.get('issues', {}),
    }
    failed = None
    try:
        for name, (original, converted) in candidates.items():
            path = VEHICLES / name
            if path.read_bytes() != original:
                raise RuntimeError(f'REFUSED: source changed during installation: {name}')
            atomic_write(path, converted)
        print(f'CABBAGE: temporarily installed {len(candidates)} candidates in original checkout', flush=True)
        if args.build:
            # CABBAGE MIGRATION SHIM: Stage 008 parity evidence must be freshly
            # generated. An incremental make install may reuse legacy PNGs/NML.
            # The project's make clean owns removal of disposable generated/;
            # generated.reference/ is NEVER a cleanup target.
            reference_dir = ROOT / 'generated.reference'
            if not reference_dir.is_dir():
                raise RuntimeError('REFUSED: missing generated.reference/ before cleanup')
            def reference_inventory():
                return {
                    p.relative_to(reference_dir).as_posix(): sha(p.read_bytes())
                    for p in reference_dir.rglob('*') if p.is_file()
                }
            reference_before = reference_inventory()
            clean_log = TRIAL_DIR / 'build_clean.log'
            print('RUN: make clean (disposable generated outputs)', flush=True)
            clean_rc = run_cmd(['make', 'clean'], clean_log)
            summary['clean'] = {
                'returncode': clean_rc,
                'log': str(clean_log.relative_to(ROOT)),
            }
            if clean_rc != 0:
                raise RuntimeError('REFUSED: make clean failed; see ' + str(clean_log))
            if reference_inventory() != reference_before:
                summary['generated_reference_modified'] = True
                raise RuntimeError('CRITICAL: make clean modified generated.reference/')
            for roster in args.rosters:
                # Prevent accidental acceptance of stale NML from a prior build.
                for extension in ('nml', 'nfo', 'grf'):
                    output = ROOT / 'generated' / f'{roster}.{extension}'
                    if output.exists():
                        if output.is_symlink() or not output.is_file():
                            raise RuntimeError(f'REFUSED: unexpected generated output: {output}')
                        output.unlink()
                cmd = ['make', 'install', f'PW={args.pw}', f'GRF={roster}']
                log = TRIAL_DIR / f'build_{roster}.log'
                print('RUN:', ' '.join(cmd), flush=True)
                build_start_ns = time.time_ns()
                rc = run_cmd(cmd, log)
                saved = snapshot_outputs(roster, build_start_ns)
                summary['builds'].append({
                    'roster': roster, 'returncode': rc,
                    'log': str(log.relative_to(ROOT)),
                    'outputs': str(saved.relative_to(ROOT)),
                    'fresh_nml': (saved / f'{roster}.nml').is_file(),
                })
                print(f'  {roster}: exit {rc}', flush=True)
    except BaseException as exc:
        failed = exc
    finally:
        # CABBAGE Restoring originals is mandatory even when build/compilation fails.
        try:
            restore_originals()
            summary['production_vehicle_files_restored'] = True
        except BaseException as restore_exc:
            print('CRITICAL: automatic vehicle restoration failed:', restore_exc, file=sys.stderr)
            print('DO NOT reset/clean the repository. Recover using --restore and retained backups.', file=sys.stderr)
            raise
        result = REPORT_DIR / 'vehicle_stage_008.json'
        result.write_text(json.dumps(summary, indent=2) + '\n', encoding='utf8')
        print('Report:', result.relative_to(ROOT), flush=True)
        if not args.retain:
            # Logs and saved outputs remain as evidence; backing originals retained
            # for crash recovery and provenance. Remove trial directory manually.
            pass
    reference_after_trial = {p.relative_to(reference_dir).as_posix(): sha(p.read_bytes())
                             for p in reference_dir.rglob('*') if p.is_file()}
    if reference_after_trial != reference_before_trial:
        summary['generated_reference_modified'] = True
        (REPORT_DIR / 'vehicle_stage_008.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf8')
        raise SystemExit('CRITICAL: generated.reference changed during Stage 008')
    if failed is not None:
        raise failed
    for item in summary['builds']:
        print('Build:', item['roster'], 'status', item['returncode'], 'log', item['log'], flush=True)
    if len(summary['builds']) != 2 or any(x['returncode'] or not x['fresh_nml'] for x in summary['builds']):
        raise SystemExit('FAIL: in-place fleet trial; see per-roster logs (vehicle sources restored)')
    print('PASS: road-hog and heqs Makefile builds; sources restored; golden reference preserved. Feature parity NOT VERIFIED')


if __name__ == '__main__':
    main()
