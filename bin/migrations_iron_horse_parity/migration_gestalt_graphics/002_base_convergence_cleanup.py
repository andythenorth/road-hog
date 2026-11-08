"""Retire GestaltGraphics row-count methods after row-type cutover."""

import ast
from pathlib import Path

TARGET = Path('src/gestalt_graphics/gestalt_graphics.py')
LEGACY = Path('src/road_vehicle/__init__.py')
PIPELINE = Path('src/gestalt_graphics/pipelines.py')


def classes(source):
    return [node for node in ast.parse(source).body if isinstance(node, ast.ClassDef)]


def remove_methods(source, names):
    lines = source.splitlines(keepends=True)
    ranges = []
    for node in classes(source):
        for child in node.body:
            if isinstance(child, ast.FunctionDef) and child.name in names:
                start = min([d.lineno for d in child.decorator_list] or [child.lineno])
                ranges.append((start, child.end_lineno))
    for start, end in sorted(ranges, reverse=True):
        del lines[start - 1:end]
    return ''.join(lines)


def main():
    source = TARGET.read_text()
    if 'def get_output_row_types(self)' not in source:
        raise RuntimeError('Run Stage 001 first')
    if 'for unit_rows in self.get_legacy_road_hog_output_row_groups(units)' in source:
        raise RuntimeError('Active consumers still require legacy row descriptors')
    # The old road_vehicle/__init__.py is retained separately. Its tuple contract
    # is not equivalent to the row-type contract, so keep the adapter explicit.
    if LEGACY.exists():
        legacy = LEGACY.read_text()
        old = 'unit_rows.extend(self.gestalt_graphics.get_output_row_counts_by_type())'
        if old in legacy:
            new = (
                '# CABBAGE: inactive legacy RoadVehicle tuple adapter; do not treat row types as counts.\n'
                '                for row_type in self.gestalt_graphics.get_output_row_types():\n'
                '                    if row_type == "livery_only":\n'
                '                        count = 3 * self.gestalt_graphics.num_cargo_sprite_variants\n'
                '                    elif row_type == "bulk_cargo":\n'
                '                        count = 2 * len(polar_fox.constants.bulk_cargo_recolour_maps)\n'
                '                    elif row_type == "piece_cargo":\n'
                '                        count = 2 * len(polar_fox.constants.piece_vehicle_type_to_sprites_maps[self.gestalt_graphics.piece_type])\n'
                '                    elif row_type == "custom_cargo":\n'
                '                        count = 2\n'
                '                    else:\n'
                '                        count = 1\n'
                '                    unit_rows.append((row_type, count))'
            )
            legacy = legacy.replace(old, new)
            ast.parse(legacy)
            LEGACY.write_text(legacy)
    source = remove_methods(source, {'get_output_row_counts_by_type', 'get_legacy_road_hog_output_row_groups'})
    if 'get_output_row_counts_by_type(' in source:
        raise RuntimeError('Unexpected remaining row-count caller in GestaltGraphics')
    # A deliberate note on the custom class, without changing its pipeline.
    marker = 'class GestaltGraphicsCustom(GestaltGraphics):'
    note = '    # CABBAGE: Road Hog custom gestalt/pipeline diverges from newer Iron Horse; consider unifying later.\n'
    if marker not in source:
        raise RuntimeError('Custom gestalt missing')
    if note not in source:
        # Insert after the class docstring rather than before (class docstring is preserved).
        tree = ast.parse(source)
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'GestaltGraphicsCustom')
        doc = cls.body[0]
        insert_line = doc.end_lineno if isinstance(doc, ast.Expr) else cls.lineno
        lines = source.splitlines(keepends=True)
        lines.insert(insert_line, note)
        source = ''.join(lines)
    if PIPELINE.exists():
        pipeline_source = PIPELINE.read_text()
        anchor = 'class CheckBuyMenuOnlyPipeline(Pipeline):'
        pipeline_note = (
            '    # CABBAGE: Road Hog custom gestalt/pipeline diverges from newer Iron Horse; '
            'consider unifying later.\n'
        )
        if anchor in pipeline_source and pipeline_note not in pipeline_source:
            pipeline_source = pipeline_source.replace(anchor, anchor + '\n' + pipeline_note, 1)
            ast.parse(pipeline_source)
            PIPELINE.write_text(pipeline_source)
    ast.parse(source)
    if source != TARGET.read_text():
        TARGET.write_text(source)
        print('Step 002: legacy row-count methods retired; custom divergence noted')
    else:
        print('Step 002: already applied')


if __name__ == '__main__':
    main()
