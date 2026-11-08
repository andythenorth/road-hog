"""Move platform spritesheet selection to the unit interface."""

import ast
from pathlib import Path

UNITS = Path('src/road_vehicle/units.py')
PIPELINE = Path('src/gestalt_graphics/pipelines.py')
OLD = '''            if self.vehicle_unit.base_platform is not None:
                spritesheet_name = self.vehicle_unit.base_platform.get_spritesheet_name_body_or_complete_vehicle(
                    self.consist
                )'''
NEW = '''            spritesheet_name = self.vehicle_unit.get_spritesheet_name_body_or_complete_vehicle()
            if spritesheet_name is not None:'''


def main():
    text = UNITS.read_text()
    method = '''    def get_spritesheet_name_body_or_complete_vehicle(self):
        return None

'''
    if method not in text:
        marker = '    def get_spriteset_template_name(self, reversed, y):'
        if marker not in text:
            raise ValueError('Unit spriteset method not found')
        text = text.replace(marker, method + marker, 1)
        ast.parse(text)
        UNITS.write_text(text)
    text = PIPELINE.read_text()
    if OLD in text:
        text = text.replace(OLD, NEW, 1)
    elif NEW not in text:
        raise ValueError('Unknown pipeline spritesheet-resolution implementation')
    # Source sheets for unit subclasses continue to reside in graphics/base_platforms.
    ast.parse(text)
    PIPELINE.write_text(text)
    print('Step 003: unit spritesheet selection active')


if __name__ == '__main__':
    main()
