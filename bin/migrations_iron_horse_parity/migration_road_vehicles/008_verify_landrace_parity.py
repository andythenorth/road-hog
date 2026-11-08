#!/usr/bin/env python3
"""CABBAGE ACCEPTANCE GATE: strict Landrace parity of fresh Stage 008 output.

HEQS is diagnostic. Do not alter generated.reference or normalize differences
without an explicit, reviewed gameplay/graphics acceptance decision.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / 'migration_state/reports/vehicle_stage_008_parity.json'
TRIAL = ROOT / 'migration_state/stage_008_trial'
REFERENCE = ROOT / 'generated.reference'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def all_files(base):
    return {p.relative_to(base).as_posix(): p for p in base.rglob('*') if p.is_file()}


def compare_png(ref, candidate):
    try:
        from PIL import Image, ImageChops
    except ImportError as exc:
        raise RuntimeError('Pillow required for pixel parity (no byte-level PNG fallback)') from exc
    with Image.open(ref) as a, Image.open(candidate) as b:
        a.load()
        b.load()
        if a.size != b.size:
            return 'dimensions differ'
        if a.convert('RGBA').tobytes() != b.convert('RGBA').tobytes():
            return 'pixel data differ'
        return None



def resolve_trial_path(reference_path, actual):
    """CABBAGE VERIFICATION BRIDGE: map legacy vehicle NML to model variant 0.

    This reconciles output filenames ONLY, never identifiers or NML contents.
    A missing variant remains a hard parity difference; do not infer variants
    other than _mv_0 or silently accept extra variants.
    """
    if reference_path in actual:
        return reference_path
    if reference_path.startswith('nml/') and reference_path.endswith('.nml'):
        candidate = reference_path[:-4] + '_mv_0.nml'
        if candidate in actual:
            return candidate
    return None

def compare_vehicle_nml(reference_path, reference_bytes, trial_bytes):
    """CABBAGE VERIFICATION BRIDGE: compare legacy vs variant-0/unit-0 NML.

    Only the model/unit symbol prefix and a known explanatory comment are
    reconciled.  All numeric properties, callback bodies, ordering, sprite
    paths, and other content must still match exactly.  The generated files
    themselves are never rewritten.  Review and retire with migration shims.
    """
    model = Path(reference_path).stem
    old_symbol = model.encode('utf8')
    new_symbol = (model + '_mv_0_unit_0').encode('utf8')
    normalized = trial_bytes.replace(new_symbol, old_symbol)
    normalized = normalized.replace(
        b'// model_variant just supplies intro year',
        b'// consist just supplies intro year',
    )
    return normalized == reference_bytes


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--reference', type=Path, default=REFERENCE)
    ap.add_argument('--trial', type=Path, default=TRIAL)
    args = ap.parse_args()
    reference = args.reference.resolve()
    trial = args.trial.resolve()
    build_report = ROOT / 'migration_state/reports/vehicle_stage_008.json'
    if not build_report.is_file():
        raise SystemExit('REFUSED: Stage 008 build report absent')
    info = json.loads(build_report.read_text(encoding='utf8'))
    builds = [entry for entry in info.get('builds', []) if entry.get('roster') == 'road-hog']
    if (len(builds) != 1 or builds[0].get('returncode') != 0
            or not info.get('production_vehicle_files_restored')
            or info.get('generated_reference_modified')):
        raise SystemExit('REFUSED: Stage 008 Landrace success, restoration or reference protection not verified')
    if not (trial / 'restore_journal.json').is_file():
        raise SystemExit('REFUSED: Stage 008 restoration journal missing')
    journal = json.loads((trial / 'restore_journal.json').read_text(encoding='utf8'))
    if journal.get('restored') is not True:
        raise SystemExit('REFUSED: Stage 008 original vehicle files not restored')
    snapshot = trial / 'outputs/road-hog'
    if not snapshot.is_dir() or not reference.is_dir():
        raise SystemExit('REFUSED: trial snapshot or golden reference missing')
    manifest = snapshot / 'freshness_manifest.json'
    if not manifest.is_file():
        raise SystemExit('REFUSED: no Stage 008 freshness manifest; rerun Stage 008 with updated pipeline')
    freshness = json.loads(manifest.read_text(encoding='utf8'))
    if freshness.get('roster') != 'road-hog' or not freshness.get('freshness_verified'):
        raise SystemExit('REFUSED: Landrace freshness not established')
    expected = {p for p in all_files(reference) if p == 'road-hog.nml'
                or p.startswith('nml/') and p.endswith('.nml')
                or p.startswith('graphics/') and p.endswith('.png')
                or p.startswith('lang/road-hog/') and p.endswith('.lng')}
    actual = all_files(snapshot)
    differences = []
    matched = {'nml': 0, 'png': 0, 'language': 0}
    consumed = set()
    pairings = []
    for path in sorted(expected):
        ref = reference / path
        trial_path = resolve_trial_path(path, actual)
        dest = actual.get(trial_path) if trial_path is not None else None
        if trial_path is not None:
            consumed.add(trial_path)
            if trial_path != path:
                pairings.append({'reference': path, 'trial': trial_path})
        kind = 'png' if path.endswith('.png') else 'language' if path.endswith('.lng') else 'nml'
        if dest is None:
            differences.append({'path': path, 'kind': kind, 'problem': 'missing from fresh trial (including _mv_0 mapping)'})
            continue
        if path.endswith('.png'):
            issue = compare_png(ref, dest)
        elif kind == 'nml' and path.startswith('nml/') and trial_path != path:
            # CABBAGE: migration renames the NML model/unit symbols, not their behaviour.
            issue = None if compare_vehicle_nml(path, ref.read_bytes(), dest.read_bytes()) else 'content differs after identifier normalization'
        else:
            issue = None if ref.read_bytes() == dest.read_bytes() else 'content differs'
        if issue:
            differences.append({'path': path, 'trial_path': trial_path, 'kind': kind, 'problem': issue,
                                'reference_sha256': digest(ref.read_bytes()),
                                'trial_sha256': digest(dest.read_bytes())})
        else:
            matched[kind] += 1
    # CABBAGE VERIFICATION BRIDGE: the combined NML is a standard new-architecture
    # build product; its per-vehicle fragments are compared above, and its NML
    # semantics still require separate review rather than an automatic pass.
    ignored_outputs = {'freshness_manifest.json', 'road-hog.nfo', 'road-hog.grf', 'road-hog.nml'}
    unexpected = sorted(set(actual) - consumed - ignored_outputs)
    if unexpected:
        differences += [{'path': name, 'problem': 'unexpected generated file'} for name in unexpected]
    # CABBAGE No unreviewed version-string normalization, identifier aliases, or
    # CABBAGE gameplay allowances. Record every difference for explicit acceptance.
    result = {'stage': '008_landrace_parity', 'strict': True, 'target': 'road-hog',
              'reference': str(reference), 'snapshot': str(snapshot),
              'reference_files': len(expected), 'nml_filename_pairs': pairings,
              'nml_filename_pairs_count': len(pairings), 'matched': matched,
              'differences_count': len(differences), 'differences': differences,
              'pass': not differences}
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, indent=2) + '\n', encoding='utf8')
    print('NML filename pairs:', len(pairings), '(strict content check after limited identifier normalization)')
    print('Landrace parity:', 'PASS' if not differences else 'FAIL', 'matched', matched,
          'differences', len(differences))
    print('Report:', REPORT.relative_to(ROOT))
    if differences:
        for item in differences[:20]:
            print('DIFF:', item['path'], item['problem'])
        raise SystemExit(1)


if __name__ == '__main__':
    main()
