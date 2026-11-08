from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GESTALT = ROOT / "src/gestalt_graphics/gestalt_graphics.py"
PIPELINE = ROOT / "src/gestalt_graphics/pipelines.py"

def main():
    source = PIPELINE.read_text()
    old = "AddBuyMenuSprite(self.process_buy_menu_sprite)"
    source = source.replace(old, "AddBuyMenuSprite(self.process_buy_menu_sprite_from_row_map)")
    start_marker = "    def process_buy_menu_sprite(self, spritesheet):"
    if start_marker in source:
        start = source.index(start_marker)
        end = source.index("    def render_common(self, input_image, units):", start)
        interim = source[start:end]
        assert "return self.process_buy_menu_sprite_from_row_map(spritesheet)" in interim, (
            "Cannot remove an unfamiliar purchase compositor"
        )
        source = source[:start] + source[end:]
    assert "AddBuyMenuSprite(self.process_buy_menu_sprite)" not in source
    assert "def process_buy_menu_sprite_from_row_map(self, spritesheet):" in source
    PIPELINE.write_text(source)
    print("Step 004: obsolete purchase renderer retired")

if __name__ == "__main__":
    main()
