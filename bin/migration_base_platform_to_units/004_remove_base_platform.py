"""Remove runtime platform resolution after unit migration."""

import ast
from pathlib import Path

CATALOGUE = Path('src/road_vehicle/catalogue.py')
MODEL = Path('src/road_vehicle/model_def.py')
UNITS = Path('src/road_vehicle/units.py')


def main():
    text = CATALOGUE.read_text()
    start = '            # CABBAGE Keep old platform override order'
    finish = '            unit = unit_cls('
    if start in text:
        left, suffix = text.split(start, 1)
        before, right = suffix.split(finish, 1)
        text = left + '            unit_cls = getattr(units, unit_def.unit_cls_name)\n' + finish + right
        text = text.replace('unit_def=resolved_def,', 'unit_def=unit_def,')
        text = text.replace('            if platform is not None:\n                unit.base_platform = platform\n', '')
        ast.parse(text)
        CATALOGUE.write_text(text)
    elif 'resolved_def' in text or 'unit.base_platform = platform' in text:
        raise ValueError('Unexpected catalogue state')
    text = MODEL.read_text()
    text = text.replace('    # CABBAGE Road Hog platform classes are still the old source of shared tractor/chassis props.\n', '')
    text = text.replace('    base_platform: Optional[Any] = None\n', '')
    ast.parse(text)
    MODEL.write_text(text)
    text = UNITS.read_text()
    text = text.replace('        # The producer sets the resolved platform instance when there is one.\n        self.base_platform = None\n', '')
    ast.parse(text)
    UNITS.write_text(text)
    # Runtime and declaration references must be gone before removing the old modules.
    for root in (Path('src/vehicles'), Path('src/road_vehicle'), Path('src/gestalt_graphics')):
        for file in root.rglob('*.py'):
            if file == Path('src/road_vehicle/__init__.py'):
                # CABBAGE: legacy Consist/RoadVehicle module is outside this migration.
                continue
            source = file.read_text()
            if 'base_platform=' in source or '.base_platform' in source or 'base_platforms.' in source:
                raise ValueError(f'Live platform dependency remains in {file}')
    Path('src/base_platform.py').unlink(missing_ok=True)
    for file in Path('src/base_platforms').glob('*.py'):
        file.unlink()
    print('Step 004: removed platform resolver and declarations')


if __name__ == '__main__':
    main()
