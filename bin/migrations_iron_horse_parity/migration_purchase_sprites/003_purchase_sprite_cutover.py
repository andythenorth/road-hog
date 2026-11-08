from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GESTALT = ROOT / "src/gestalt_graphics/gestalt_graphics.py"
PIPELINE = ROOT / "src/gestalt_graphics/pipelines.py"

def main():
    source = PIPELINE.read_text()
    if "def process_buy_menu_sprite(self, spritesheet):" not in source:
        assert "def process_buy_menu_sprite_from_row_map(self, spritesheet):" in source
        print("Step 003: superseded by Step 004")
        return
    assert "def process_buy_menu_sprite_from_row_map(self, spritesheet):" in source
    start = source.index("    def process_buy_menu_sprite(self, spritesheet):")
    end = source.index("    def render_common(self, input_image, units):", start)
    replacement = '    def process_buy_menu_sprite(self, spritesheet):\n        # CABBAGE: temporary compatibility entry point; Step 004 retires it.\n        return self.process_buy_menu_sprite_from_row_map(spritesheet)\n\n'
    existing = source[start:end]
    if existing != replacement:
        source = source[:start] + replacement + source[end:]
        PIPELINE.write_text(source)
    print("Step 003: purchase renderer uses strategy row maps")

if __name__ == "__main__":
    main()
