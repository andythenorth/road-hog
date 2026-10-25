#!/usr/bin/env python3
"""Stage 008 Pass 1 structural acceptance; NOT full Landrace gameplay parity.

CABBAGE: Pass 1 intentionally supports vehicle_default.pynml only.
Cargo-specific livery and visible-cargo templates require a later migration.
This gate NEVER treats a passing build as evidence of gameplay property parity.
The strict Landrace parity verifier remains independently runnable.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / 'migration_state' / 'reports'
TRIAL = ROOT / 'migration_state' / 'stage_008_trial'


def assess(info, journal, freshness, candidates):
    builds = {b.get('roster'): b for b in info.get('builds', [])}
    checks = {
        '132_migration_candidates': candidates == 132,
        'road_hog_build': builds.get('road-hog', {}).get('returncode') == 0 and builds.get('road-hog', {}).get('fresh_nml') is True,
        'heqs_build': builds.get('heqs', {}).get('returncode') == 0 and builds.get('heqs', {}).get('fresh_nml') is True,
        'production_vehicle_sources_restored': info.get('production_vehicle_files_restored') is True and journal.get('restored') is True,
        'golden_reference_untouched': info.get('generated_reference_modified') is False,
        'fresh_road_hog_snapshot': freshness.get('roster') == 'road-hog' and freshness.get('freshness_verified') is True,
    }
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    reports = root / 'migration_state' / 'reports'
    trial = root / 'migration_state' / 'stage_008_trial'
    paths = [reports / 'vehicle_stage_008.json', trial / 'restore_journal.json',
             trial / 'outputs' / 'road-hog' / 'freshness_manifest.json']
    missing = [str(p) for p in paths if not p.is_file()]
    if missing:
        raise SystemExit('REFUSED: missing Stage 008 evidence: ' + ', '.join(missing))
    info, journal, freshness = [json.loads(p.read_text(encoding='utf8')) for p in paths]
    checks = assess(info, journal, freshness, info.get('candidate_count'))
    # Deliberate separation: content parity is not silently waived. It is NOT
    # part of this structural pass and must be resolved prior to fleet cutover.
    result = {
        'stage': '008_pass1_structural',
        'scope': 'structural_build_and_restoration_only',
        'pass': all(checks.values()),
        'checks': checks,
        'templates_in_scope': ['vehicle_default.pynml'],
        'templates_deferred_CABBAGE': ['vehicle_with_cargo_specific_liveries.pynml', 'vehicle_with_visible_cargo.pynml'],
        'gameplay_parity_verified': False,
        'cutover_approved': False,
        'strict_parity_report': 'migration_state/reports/vehicle_stage_008_parity.json',
        'note': 'PASS does not certify gameplay, visual effects, NML, PNG or language equivalence.',
    }
    out = reports / 'vehicle_stage_008_pass1.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf8')
    print('Stage 008 Pass 1 structural:', 'PASS' if result['pass'] else 'FAIL')
    print('Gameplay parity: UNVERIFIED (separate strict gate)')
    print('Report:', out)
    if not result['pass']:
        for key, value in checks.items():
            if not value:
                print('FAIL:', key)
        raise SystemExit(1)


if __name__ == '__main__':
    main()
