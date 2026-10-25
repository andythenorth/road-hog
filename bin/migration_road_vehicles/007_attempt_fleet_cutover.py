#!/usr/bin/env python3
"""Attempt the whole-fleet cutover; never install a fleet with unresolved contracts.

CABBAGE This is intentionally a guarded attempt, not a claim of NML parity.
"""
from __future__ import annotations
import argparse
import ast
from collections import Counter
from dataclasses import fields
import hashlib
import io
import json
from pathlib import Path
import shutil
import sys
import tokenize

ROOT = Path(__file__).resolve().parents[2]
VEHICLES = ROOT / 'src/vehicles'
SCHEMAS = ROOT / 'src/road_vehicle/schemas.py'
MODEL = ROOT / 'src/road_vehicle/model_def.py'
UNITS = ROOT / 'src/road_vehicle/units.py'
OUT = ROOT / 'migration_state/vehicle_cutover_candidates'
REPORT = ROOT / 'migration_state/reports/vehicle_stage_007.json'


def node_text(source, node):
    return ast.get_source_segment(source, node)


def offsets(source):
    p = [0]
    for line in source.splitlines(keepends=True): p.append(p[-1]+len(line))
    return p


def bounds(node, pos):
    return pos[node.lineno-1]+node.col_offset, pos[node.end_lineno-1]+node.end_col_offset


def comments(source):
    return [t.string for t in tokenize.generate_tokens(io.StringIO(source).readline) if t.type == tokenize.COMMENT]


def class_names(tree):
    return {n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)}


def model_fields(tree, name):
    for n in tree.body:
        if isinstance(n, ast.ClassDef) and n.name == name:
            return {x.target.id for x in n.body if isinstance(x, ast.AnnAssign) and isinstance(x.target, ast.Name)}
    raise ValueError(f'Missing {name} dataclass')


def roster_keyword_edit(source, kw, pos, constructor):
    """Remove a standalone legacy roster kw without consuming nearby comments.

    The common Black-formatted case is one keyword per line. A nonstandard
    layout is left untouched and reported rather than guessed at.
    """
    if not isinstance(kw.value, ast.Name) or kw.value.id != 'roster_id':
        return None
    start, end = bounds(kw, pos)
    line_start = source.rfind('\n', 0, start) + 1
    line_end = source.find('\n', end)
    if line_end < 0:
        line_end = len(source)
    before = source[line_start:start]
    after = source[end:line_end]
    # Inline argument followed by another keyword on the same line.
    later = [k for k in constructor.keywords if k is not kw and bounds(k, pos)[0] > start]
    if later:
        following = min(bounds(k, pos)[0] for k in later)
        import re
        if re.fullmatch(r',[ \t]*', source[end:following]):
            return (start, following, '')
    if before.strip():
        return None
    # A trailing comment is kept exactly; do not move it onto another kw.
    import re
    match = re.fullmatch(r'([ \t]*),([ \t]*)(#.*)?', after)
    if match is None:
        return None
    if match.group(3) is None:
        # Consume the whole line including its newline.
        return (line_start, line_end + (line_end < len(source)), '')
    # Keep the comment on its own line, including its existing indentation.
    return (start, end + len(match.group(1)) + 1 + len(match.group(2)), '')


def obsolete_sprite_row_edit(source, kw, pos):
    """Comment out only a standalone legacy keyword, without losing source text.

    CABBAGE: This old sprite-row override is intentionally not part of UnitDef.
    Refuse nonstandard layouts rather than risk corrupting adjacent arguments.
    """
    start, end = bounds(kw, pos)
    line_start = source.rfind('\n', 0, start) + 1
    line_end = source.find('\n', end)
    if line_end == -1:
        line_end = len(source)
    indent = source[line_start:start]
    tail = source[end:line_end]
    import re
    if not re.fullmatch(r'[ \t]*', indent):
        return None
    if not re.fullmatch(r',?[ \t]*(?:#.*)?', tail):
        return None
    # Preserve the full original line (including its own comment), but disable
    # its keyword by prefixing a CABBAGE marker after the original indentation.
    return (line_start, line_end, indent + '# CABBAGE ' + source[start:line_end])


def convert(path, available_schemas, available_units, model_keys, unit_keys):
    original = path.read_text(encoding='utf-8')
    entry = {'file': path.name, 'issues': [], 'units': 0, 'obsolete_sprite_row_overrides_commented': 0, 'legacy_running_cost_overrides_commented': 0, 'schema': None, 'source_sha256': hashlib.sha256(original.encode()).hexdigest()}
    issues = entry['issues']
    tree = ast.parse(original, filename=str(path))
    if 'ModelDef(' in original:
        entry['status'] = 'already_model_def'
        return entry, None
    main = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'main']
    if len(main) != 1:
        issues.append('expected_one_main')
        entry['status'] = 'blocked'
        return entry, None
    fn = main[0]
    assignments = [(n, n.value) for n in ast.walk(fn) if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id == 'consist' and isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Name)]
    if len(assignments) != 1:
        issues.append('expected_one_consist_assignment')
        entry['status'] = 'blocked'
        return entry, None
    assn, ctor = assignments[0]
    legacy_cls = ctor.func.id
    # CABBAGE: The already-migrated local bus schema is named Bus.
    # Keep this exception in the source converter, not as a redundant schema.
    schema = 'Bus' if legacy_cls == 'PaxLocalBusConsist' else legacy_cls.removesuffix('Consist')
    # CABBAGE
    # Legacy *Base is already an explicit schema class, not a suffix to delete.
    entry['schema'] = schema
    if schema not in available_schemas:
        issues.append('schema_absent:' + schema)
    pos = offsets(original)
    edits = []
    def edit(node, value):
        a, b = bounds(node, pos)
        edits.append((a, b, value))
    edit(assn.targets[0], 'model_def')
    edit(ctor.func, 'ModelDef')
    keywords = {k.arg: k for k in ctor.keywords if k.arg}
    retired_inline_comments = []
    if len(keywords) != len(ctor.keywords): issues.append('constructor_unpack')
    # The new catalogue owns the roster id, as it does for the Leyburn fixture.
    for kw in ctor.keywords:
        if kw.arg == 'id':
            edit(kw, 'model_id=' + node_text(original, kw.value))
        elif kw.arg == 'intro_date_offset':
            edit(kw, 'intro_year_offset=' + node_text(original, kw.value))
        elif kw.arg == 'roster_id':
            removal = roster_keyword_edit(original, kw, pos, ctor)
            if removal is None:
                issues.append('roster_id_removal_needs_token_safe_edit')
            else:
                edits.append(removal)
        elif kw.arg == 'type_base_running_cost_points':
            # CABBAGE: These two historic cost dials have been retired deliberately.
            # Keep the source and inline balance notes readable, never map their values
            # to the new fixed_run_cost_points API (different cost semantics).
            removal = obsolete_sprite_row_edit(original, kw, pos)
            if removal is None:
                issues.append('legacy_running_cost_override_needs_manual_review')
            else:
                edits.append(removal)
                entry['legacy_running_cost_overrides_commented'] += 1
                # This inline comment becomes part of the whole-line CABBAGE
                # comment. Track it for the comment preservation check below.
                line_end = original.find('\n', bounds(kw, pos)[1])
                if line_end < 0: line_end = len(original)
                segment = original[bounds(kw, pos)[1]:line_end]
                if '#' in segment:
                    retired_inline_comments.append(segment[segment.index('#'):].strip())
        elif kw.arg == 'power':
            # Legacy power is a scalar; cannot silently choose steam/diesel/electric.
            issues.append('power_source_unresolved')
        elif kw.arg and kw.arg not in model_keys:
            issues.append('unsupported_model_kw:' + kw.arg)
    if 'gen' not in keywords:
        issues.append('gen_missing')
    if 'schema_name' not in keywords:
        # Insertion is safe directly after the '(' rather than modifying caller formatting.
        a, _ = bounds(ctor, pos)
        # Parenthesized call: find opening parenthesis after function name.
        start, end = bounds(ctor.func, pos)
        paren = original.find('(', end, end + 16)
        if paren < 0: issues.append('constructor_open_paren_not_found')
        else: edits.append((paren+1, paren+1, f'schema_name={schema!r}, '))
    for n in ast.walk(fn):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == 'add_unit':
            if not isinstance(n.func.value, ast.Name) or n.func.value.id != 'consist':
                issues.append('nonlocal_add_unit')
                continue
            entry['units'] += 1
            edit(n.func, 'model_def.add_unit_def')
            unit_kw = {k.arg: k for k in n.keywords if k.arg}
            if 'type' not in unit_kw:
                issues.append('unit_class_inferred_legacy_default')
                # The legacy default is RoadVehicle; the model unit is RoadVehicleUnit.
                p, _ = bounds(n.func, pos)
                paren = original.find('(', bounds(n.func, pos)[1], bounds(n.func, pos)[1]+16)
                if paren >= 0: edits.append((paren+1, paren+1, "unit_cls_name='RoadVehicleUnit', "))
            for kw in n.keywords:
                if kw.arg == 'type':
                    if isinstance(kw.value, ast.Name):
                        unit_name = kw.value.id
                        if unit_name not in available_units: issues.append('unit_class_absent:' + unit_name)
                        edit(kw, 'unit_cls_name=' + repr(unit_name))
                    else: issues.append('dynamic_unit_class')
                elif kw.arg == 'unit_num_providing_spriterow_num':
                    # CABBAGE: Legacy sprite-row sharing is obsolete. Keep the
                    # original caller visible in comments, never extend UnitDef.
                    removal = obsolete_sprite_row_edit(original, kw, pos)
                    if removal is None:
                        issues.append('obsolete_sprite_row_override_needs_manual_review')
                    else:
                        edits.append(removal)
                        entry['obsolete_sprite_row_overrides_commented'] += 1
                elif kw.arg is None:
                    issues.append('unit_unpack')
                elif kw.arg not in unit_keys:
                    issues.append('unsupported_unit_kw:' + str(kw.arg))
        if isinstance(n, ast.Return) and isinstance(n.value, ast.Name) and n.value.id == 'consist':
            edit(n.value, '[model_def]')
    if not entry['units']: issues.append('no_units')
    # Import belongs after existing imports so it does not violate __future__ imports.
    imports = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))]
    import_at = pos[imports[-1].end_lineno] if imports else 0
    # CABBAGE: Retain deferred rendering scope beside each migrated vehicle.
    # Stage 008 may restore originals after its trial; installed candidates keep it.
    edits.append((import_at, import_at,
        '\nfrom road_vehicle.model_def import ModelDef\n'
        '# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.\n'
        '# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific\n'
        '# spritegroups/liveries where present in this vehicle.\n'))
    edits.sort(key=lambda x: (x[0], x[1]), reverse=True)
    candidate = original
    next_end = len(original)+1
    for a, b, value in edits:
        if b > next_end:
            issues.append('overlapping_edits')
            entry['status'] = 'blocked'
            return entry, None
        candidate = candidate[:a] + value + candidate[b:]
        next_end = a
    try: ast.parse(candidate)
    except SyntaxError as exc: issues.append('candidate_syntax_error:' + str(exc.lineno))
    # CABBAGE comments contain formerly active source lines, not old comments.
    old_comments = comments(original)
    for retired_comment in retired_inline_comments:
        old_comments.remove(retired_comment)
    new_comments = [c for c in comments(candidate) if not (
        c.startswith('# CABBAGE unit_num_providing_spriterow_num=') or
        c.startswith('# CABBAGE type_base_running_cost_points=') or
        c.startswith('# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.') or
        c.startswith('# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific') or
        c.startswith('# spritegroups/liveries where present in this vehicle.'))]
    if old_comments != new_comments: issues.append('comments_changed')
    # Existing legacy imports remain in candidates; importing from road_vehicle is
    # deliberately not treated as production-ready.
    issues.append('legacy_import_cleanup_required')
    issues.append('runtime_and_golden_parity_unverified')
    entry['status'] = 'blocked' if issues else 'ready'
    return entry, candidate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--install', action='store_true', help='install only if *all* contracts pass')
    args = parser.parse_args()
    for p in [VEHICLES, SCHEMAS, MODEL, UNITS]:
        if not p.exists(): raise SystemExit(f'Missing required path: {p}')
    schema_names = class_names(ast.parse(SCHEMAS.read_text()))
    unit_names = class_names(ast.parse(UNITS.read_text()))
    required_power_units = {'SteamVehicleUnit', 'DieselVehicleUnit', 'ElectricVehicleUnit'}
    missing_power_units = required_power_units - unit_names
    if missing_power_units:
        raise SystemExit('Stage 005/006 unit provision incomplete: ' + repr(sorted(missing_power_units)))
    model_tree = ast.parse(MODEL.read_text())
    model_class = next(n for n in model_tree.body if isinstance(n, ast.ClassDef) and n.name == 'ModelDef')
    sprites_fields = [n for n in model_class.body if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name) and n.target.id == 'sprites_complete']
    if len(sprites_fields) != 1 or not isinstance(sprites_fields[0].value, ast.Constant) or sprites_fields[0].value.value is not False:
        raise SystemExit('Stage 001 required: sprites_complete must default to False before Stage 007')
    model_keys = model_fields(model_tree, 'ModelDef')
    if 'fixed_run_cost_points' not in model_keys:
        raise SystemExit('Iron Horse ModelDef fixed_run_cost_points field missing; foundation requires review')
    unit_keys = model_fields(model_tree, 'UnitDef')
    OUT.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    results, candidates = [], {}
    for path in sorted(VEHICLES.glob('*.py')):
        if path.name == '__init__.py': continue
        try: entry, candidate = convert(path, schema_names, unit_names, model_keys, unit_keys)
        except Exception as exc:
            entry, candidate = {'file': path.name, 'status': 'blocked', 'issues': ['conversion_exception:' + repr(exc)]}, None
        results.append(entry)
        if candidate is not None:
            (OUT/path.name).write_text(candidate, encoding='utf-8')
            candidates[path.name] = candidate
    breakdown = Counter(i.split(':')[0] for row in results for i in row['issues'])
    blocked = [r for r in results if r['status'] == 'blocked']
    report = {'stage': 7, 'vehicle_files': len(results), 'candidate_files': len(candidates), 'blocked_files': len(blocked), 'obsolete_sprite_row_overrides_commented': sum(r.get('obsolete_sprite_row_overrides_commented', 0) for r in results), 'legacy_running_cost_overrides_commented': sum(r.get('legacy_running_cost_overrides_commented', 0) for r in results), 'issues': dict(breakdown), 'files': results}
    REPORT.write_text(json.dumps(report, indent=2) + '\n')
    print(f'Stage 007: {len(results)} files, {len(candidates)} candidate drafts, {len(blocked)} blocked')
    print('  obsolete_sprite_row_overrides_commented:', report['obsolete_sprite_row_overrides_commented'])
    print('  legacy_running_cost_overrides_commented:', report['legacy_running_cost_overrides_commented'])
    for key, count in breakdown.most_common(): print(f'  {key}: {count}')
    print('Report:', REPORT.relative_to(ROOT))
    if blocked:
        if args.install: raise SystemExit('REFUSED: unresolved migration contracts; no production files changed')
        print('PASS: guarded cutover preflight completed; production files unchanged')
        return
    if args.install:
        # Source hashes prevent overwriting any file changed during preparation.
        for entry in results:
            p = VEHICLES / entry['file']
            if hashlib.sha256(p.read_bytes()).hexdigest() != entry['source_sha256']:
                raise SystemExit('REFUSED: source changed: ' + entry['file'])
        # Backups before writes, then atomically replace the edited fleet.
        backup = ROOT / 'migration_state/vehicle_cutover_backup'
        if backup.exists(): raise SystemExit('REFUSED: backup already exists')
        backup.mkdir(parents=True)
        for name in candidates: shutil.copy2(VEHICLES/name, backup/name)
        for name, candidate in candidates.items():
            tmp = (VEHICLES/name).with_suffix('.stage007.tmp')
            tmp.write_text(candidate)
            tmp.replace(VEHICLES/name)
        print('INSTALLED: candidate vehicle files. Original files at', backup)
    else:
        print('PASS: all candidate contracts passed; rerun --install to install')


if __name__ == '__main__': main()
