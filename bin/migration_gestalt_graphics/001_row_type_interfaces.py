"""Migrate active Road Hog GestaltGraphics row consumers to row-type names."""

import ast
from pathlib import Path

TARGET = Path('src/gestalt_graphics/gestalt_graphics.py')


def method_bounds(source, class_name, method_name):
    tree = ast.parse(source)
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) and child.name == method_name:
                    return child.lineno, child.end_lineno
    return None


def replace_method(source, class_name, method_name, replacement):
    bounds = method_bounds(source, class_name, method_name)
    if not bounds:
        raise RuntimeError(f'Missing {class_name}.{method_name}')
    lines = source.splitlines(keepends=True)
    start, end = bounds
    lines[start - 1:end] = [replacement]
    return ''.join(lines)


def insert_after_method(source, class_name, method_name, addition):
    bounds = method_bounds(source, class_name, method_name)
    if not bounds:
        raise RuntimeError(f'Missing {class_name}.{method_name}')
    lines = source.splitlines(keepends=True)
    lines.insert(bounds[1], '\n' + addition)
    return ''.join(lines)


def main():
    source = TARGET.read_text()
    if not method_bounds(source, 'GestaltGraphics', 'get_output_row_types'):
        source = insert_after_method(
            source, 'GestaltGraphics', 'get_output_row_counts_by_type',
            '    def get_output_row_types(self):\n'
            '        return ["single_row"]\n',
        )
    for class_name, result in (
        ('GestaltGraphicsLiveryOnly', '["livery_only"]'),
        ('GestaltGraphicsCustom', '["empty", "custom_cargo"]'),
    ):
        if not method_bounds(source, class_name, 'get_output_row_types'):
            source = insert_after_method(
                source, class_name, 'get_output_row_counts_by_type',
                f'    def get_output_row_types(self):\n        return {result}\n',
            )
    source = replace_method(
        source, 'GestaltGraphics', 'get_spriterow_types_for_units',
        '    def get_spriterow_types_for_units(self, units):\n'
        '        return [\n'
        '            ["always_use_same_spriterow"]\n'
        '            if unit.always_use_same_spriterow\n'
        '            else self.get_output_row_types()\n'
        '            for unit in units\n'
        '        ]\n',
    ) if 'for unit_rows in self.get_legacy_road_hog_output_row_groups(units)' in source else source
    ast.parse(source)
    if source != TARGET.read_text():
        TARGET.write_text(source)
        print('Step 001: row-type producers and active consumers migrated')
    else:
        print('Step 001: already applied')


if __name__ == '__main__':
    main()
