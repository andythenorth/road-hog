#!/usr/bin/env python3
"""Stage 2: activate Iron Horse-style variant groups for Road Hog NML.

Run from the Road Hog repository root, after applying Stage 1.
Only src/render_nml.py and src/templates/properties.pynml are modified.
"""

from pathlib import Path

ROOT = Path.cwd()
RENDER = ROOT / 'src/render_nml.py'
PROPERTIES = ROOT / 'src/templates/properties.pynml'
ROSTER = ROOT / 'src/roster.py'
SCHEMAS = ROOT / 'src/road_vehicle/schemas.py'
CATALOGUE = ROOT / 'src/road_vehicle/catalogue.py'


def require_stage1():
    checks = (
        (ROSTER, 'def add_variant_groups(self):'),
        (ROSTER, 'class VariantGroup(list):'),
        (SCHEMAS, 'def variant_group_as_nml_prop(self):'),
        (CATALOGUE, 'def get_variant_group_id(self, livery_def):'),
    )
    for path, marker in checks:
        if not path.is_file() or marker not in path.read_text(encoding='utf-8'):
            raise RuntimeError(f'Stage 1 prerequisite missing: {marker} in {path}')


def render_change(source):
    before = '    road_hog.main()'
    after = '    road_hog.main(run_post_validation_steps=True)'
    if after in source and before not in source:
        return source
    if source.count(before) != 1:
        raise RuntimeError('Expected exactly one unmodified road_hog.main() call in render_nml.py')
    return source.replace(before, after, 1)


def properties_change(source):
    block = (
        '            <tal:variant_group condition="model_variant.variant_group_as_nml_prop is not None">\n'
        '                variant_group:                  ${model_variant.variant_group_as_nml_prop};\n'
        '            </tal:variant_group>\n'
    )
    if block in source:
        return source
    if 'variant_group:' in source:
        raise RuntimeError('An existing variant_group property needs manual review')
    anchor = '            retire_early:                   ${model_variant.retire_early};\n'
    if source.count(anchor) != 1:
        raise RuntimeError('Expected exactly one retire_early property in properties.pynml')
    return source.replace(anchor, anchor + block, 1)


def main():
    require_stage1()
    render_source = RENDER.read_text(encoding='utf-8')
    props_source = PROPERTIES.read_text(encoding='utf-8')
    new_render = render_change(render_source)
    new_props = properties_change(props_source)
    compile(new_render, str(RENDER), 'exec')
    for path, old, new in (
        (RENDER, render_source, new_render),
        (PROPERTIES, props_source, new_props),
    ):
        if old != new:
            path.write_text(new, encoding='utf-8')
            print(f'Updated {path.relative_to(ROOT)}')
        else:
            print(f'Already aligned: {path.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
