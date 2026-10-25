#!/usr/bin/env python3
"""Stage 009: port opt-in Road Hog cargo-rendering templates and model contract.

CABBAGE: This stage adds rendering capability without inferring legacy cargo maps.
Existing vehicle declarations remain default-template until explicitly configured.
Re-run after Stage 001-007; idempotent. No production vehicle file changes.
"""
from __future__ import annotations
import argparse
import ast
import json
import re
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_NAMES = ('vehicle_with_cargo_specific_liveries.pynml', 'vehicle_with_visible_cargo.pynml')


def insert_field(text):
    marker = '    # CABBAGE STAGE 009: Explicit cargo graphics metadata; no inferred legacy maps.\n'
    if marker in text:
        return text
    tree = ast.parse(text)
    model = next((node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == 'ModelDef'), None)
    if not model:
        raise ValueError('ModelDef class not found')
    field = next((node for node in model.body if isinstance(node, ast.AnnAssign) and getattr(node.target, 'id', None) == 'sprites_complete'), None)
    if not field:
        raise ValueError('ModelDef.sprites_complete not found')
    lines = text.splitlines(keepends=True)
    lines.insert(field.end_lineno, marker +
        '    graphics_template: str = "vehicle_default.pynml"\n'
        '    cargo_row_map: Optional[Dict[str, List[int]]] = None\n'
        '    num_cargo_sprite_variants: Optional[int] = None\n'
        '    generic_rows: Optional[List[int]] = None\n'
        '    cargo_random_switch_expressions: Optional[Dict[str, str]] = None\n')
    result = ''.join(lines)
    ast.parse(result)
    return result


def insert_render_selection(text):
    # CABBAGE: Stage 006 emits the selector without fixed whitespace; match syntax, not formatting.
    selector = re.compile(r"(?m)^(?P<indent>[ \t]*)template\s*=\s*templates\s*\[\s*[\"\']vehicle_default\.pynml[\"\']\s*\][ \t]*$")
    marker = '            # CABBAGE STAGE 009: Explicit opt-in cargo graphics templates.'
    if marker in text:
        return text
    matches = list(selector.finditer(text))
    if len(matches) != 1:
        raise ValueError('Expected precisely one default rendering selector; found %d' % len(matches))
    new = """            # CABBAGE STAGE 009: Explicit opt-in cargo graphics templates.
            choice = self.model_def.graphics_template
            supported = ('vehicle_default.pynml', 'vehicle_with_cargo_specific_liveries.pynml',
                         'vehicle_with_visible_cargo.pynml')
            if choice not in supported:
                raise ValueError('Unsupported vehicle template: ' + str(choice))
            if choice != 'vehicle_default.pynml':
                mapping = self.model_def.cargo_row_map
                count = self.model_def.num_cargo_sprite_variants
                if not isinstance(mapping, dict) or not mapping or not isinstance(count, int) or count < 1:
                    raise ValueError('CABBAGE: cargo graphics require explicit row mapping and sprite variant count')
                if 'DFLT' not in mapping and choice == 'vehicle_with_cargo_specific_liveries.pynml':
                    raise ValueError('CABBAGE: livery-only templates require DFLT mapping')
                for cargo, rows in mapping.items():
                    if not isinstance(cargo, str) or not rows or any(type(n) is not int or n < 0 or n >= count for n in rows):
                        raise ValueError('Invalid cargo sprite rows for ' + repr(cargo))
                if choice == 'vehicle_with_visible_cargo.pynml':
                    generic = self.model_def.generic_rows
                    expressions = self.model_def.cargo_random_switch_expressions
                    if not generic or not isinstance(expressions, dict) or not all(
                        key in expressions for key in list(mapping) + ['generic_cargos']
                    ):
                        raise ValueError('CABBAGE: visible cargo needs explicit generic rows and random switch expressions')
                    if any(type(n) is not int or n < 0 or n >= count for n in generic):
                        raise ValueError('Invalid visible-cargo generic sprite rows')
            template = templates[choice]"""
    # Match the actual indent so Stage 009 works with generated schemas.
    indent = matches[0].group("indent")
    new = "\n".join((indent + line.lstrip() if i == 0 else indent + line[12:] if line.startswith("            ") else indent + line) for i, line in enumerate(new.splitlines()))
    result = text[:matches[0].start()] + new + text[matches[0].end():]
    ast.parse(result)
    return result


def render_contract(source):
    # The template uses the model definition's explicit graphics mapping; it never
    # imports Consist or uses legacy gestalt objects.
    return source


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=ROOT)
    args = p.parse_args()
    root = args.root.resolve()
    model = root / 'src/road_vehicle/model_def.py'
    schemas = root / 'src/road_vehicle/schemas.py'
    templates = root / 'src/templates'
    for path in (model, schemas):
        if not path.is_file():
            raise SystemExit('Missing Stage 001/006 source: ' + str(path))
    inputs = {model: model.read_text(encoding='utf8'), schemas: schemas.read_text(encoding='utf8')}
    modifications = {model: insert_field(inputs[model]), schemas: insert_render_selection(inputs[schemas])}
    for path, value in modifications.items():
        ast.parse(value, filename=str(path))
    source_dir = Path(__file__).with_name('stage009_templates')
    staged = {}
    for name in TEMPLATE_NAMES:
        path = source_dir / name
        if not path.is_file():
            raise SystemExit('Missing packaged template: ' + str(path))
        staged[templates / name] = path.read_bytes()
    # Fail closed on unexpected pre-existing template edits.
    for path, content in staged.items():
        if path.is_file() and path.read_bytes() != content:
            original = path.read_text(encoding='utf8')
            if 'consist.gestalt_graphics' not in original and '${vehicle.id}' not in original:
                raise SystemExit('REFUSED: unknown template modification: ' + str(path))
    for path, value in modifications.items():
        if path.read_text(encoding='utf8') != value:
            path.write_text(value, encoding='utf8')
    templates.mkdir(parents=True, exist_ok=True)
    for path, content in staged.items():
        if not path.is_file() or path.read_bytes() != content:
            path.write_bytes(content)
    report = {'stage': 9, 'pass': True, 'scope': 'template_infrastructure_only',
              'templates': list(TEMPLATE_NAMES), 'configured_vehicle_count': 0,
              'vehicle_graphics_parity_verified': False,
              'note': 'No vehicle is automatically opted in; legacy cargo maps require explicit migration.'}
    dest = root / 'migration_state/reports/vehicle_stage_009.json'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(report, indent=2) + '\n', encoding='utf8')
    print('PASS: Stage 009 template infrastructure installed. Per-vehicle mapping remains CABBAGE.')

if __name__ == '__main__':
    main()
