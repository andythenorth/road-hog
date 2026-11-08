from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GESTALT = ROOT / "src/gestalt_graphics/gestalt_graphics.py"
PIPELINE = ROOT / "src/gestalt_graphics/pipelines.py"

def main():
    source = PIPELINE.read_text()
    marker = "    def process_buy_menu_sprite_from_row_map(self, spritesheet):"
    if marker not in source:
        anchor = "    def process_buy_menu_sprite(self, spritesheet):"
        assert source.count(anchor) == 1, "Unexpected Road Hog compositor layout"
        source = source.replace(anchor, '    def process_buy_menu_sprite_from_row_map(self, spritesheet):\n        # Adapted from Iron Horse\'s row-map compositor. Road Hog retains its\n        # purchase-sprite destination and semi-tractor geometry.\n        buy_menu_image = Image.new(\n            "P", (self.consist.buy_menu_width, self.global_constants.docs_sprite_height), 0\n        )\n        buy_menu_image.putpalette(DOS_PALETTE)\n        for row_data in self.consist.gestalt_graphics.buy_menu_row_map(self):\n            if row_data["spriterow_num_dest"] != 0:\n                raise ValueError("Road Hog currently supports one purchase sprite row")\n            x_offset = 0\n            for unit, input_row_num in row_data[\n                "source_vehicles_and_input_spriterow_nums"\n            ]:\n                if unit.unit_is_semi_tractor:\n                    unit_width = 6 * (\n                        unit.vehicle_length + unit.semi_truck_shift_offset_jank\n                    )\n                    increment = 6 * unit.vehicle_length\n                else:\n                    unit_width = 4 * unit.vehicle_length\n                    increment = unit_width\n                row_y = input_row_num * graphics_constants.spriterow_height\n                sprite = spritesheet.sprites.crop(\n                    (227, 10 + row_y, 228 + unit_width, 26 + row_y)\n                )\n                mask = sprite.point(lambda pixel: 0 if pixel == 0 else 255).convert("1")\n                buy_menu_image.paste(sprite, (x_offset, 0), mask)\n                x_offset += increment\n        spritesheet.sprites.paste(\n            buy_menu_image, (self.consist.buy_menu_x_loc, 10)\n        )\n        return spritesheet\n\n' + anchor, 1)
        PIPELINE.write_text(source)
    print("Step 002: row-map purchase compositor available")

if __name__ == "__main__":
    main()
