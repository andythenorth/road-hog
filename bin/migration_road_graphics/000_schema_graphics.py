"""Give the road schema the graphics settings used by the old Road Hog renderer."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / 'src/road_vehicle/schemas.py'


def main():
    text = PATH.read_text()
    old_import = 'import road_hog\n'
    new_import = 'import road_hog\nfrom gestalt_graphics.gestalt_graphics import GestaltGraphics\n'
    old_fields = '        self.units = []\n        self.id = catalogue_entry.model_variant_id\n'
    new_fields = '''        self.units = []
        self.id = catalogue_entry.model_variant_id
        # The normal bus sprite pipeline just reads and writes the sprite sheet.
        # Other graphics types can choose a different GestaltGraphics later.
        self.gestalt_graphics = GestaltGraphics()
        self.sprites_complete = bool(getattr(self.model_def, "sprites_complete", False))
        self.sprites_additional_liveries_potential = False
        # CABBAGE Sprite file names still use the base model id, not variant ids.
        # Check this when model variants get different graphics/liveries.
        self.graphics_file_id = self.model_def.model_id
'''
    if new_import not in text:
        if text.count(old_import) != 1:
            raise RuntimeError('Unexpected schema imports; review before editing')
        text = text.replace(old_import, new_import, 1)
    if new_fields not in text:
        if text.count(old_fields) != 1:
            raise RuntimeError('Unexpected schema constructor; review before editing')
        text = text.replace(old_fields, new_fields, 1)
    PATH.write_text(text)
    print('PASS: schema provides default graphics settings and legacy sprite file identity')


if __name__ == '__main__':
    main()
