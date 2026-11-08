from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GESTALT = ROOT / "src/gestalt_graphics/gestalt_graphics.py"
PIPELINE = ROOT / "src/gestalt_graphics/pipelines.py"

def main():
    source = GESTALT.read_text()
    if "def buy_menu_row_map(self, pipeline):" not in source:
        anchor = "    @property\n    def nml_template(self):"
        assert anchor in source, "Missing GestaltGraphics base anchor"
        addition = '    def get_buy_menu_unit_input_row_num(self, pipeline, unit):\n        return unit.spriterow_num\n\n    def buy_menu_row_map(self, pipeline):\n        # Iron Horse row-map contract, adapted to Road Hog\'s single purchase row.\n        return [\n            {\n                "spriterow_num_dest": 0,\n                "source_vehicles_and_input_spriterow_nums": [\n                    (unit, self.get_buy_menu_unit_input_row_num(pipeline, unit))\n                    for unit in pipeline.consist.units\n                ],\n            }\n        ]\n\n'
        source = source.replace(anchor, addition + anchor, 1)
    if "def get_buy_menu_unit_input_row_num(self, pipeline, unit):" not in source:
        raise RuntimeError("Missing expected base strategy interface")
    class_anchor = "class GestaltGraphicsPrecompositedCargo(GestaltGraphics):"
    if "# Output row ownership is defined by GestaltGraphics, not unit indices." not in source:
        assert source.count(class_anchor) == 1
        # Attach the override to the precomposited strategy, not the base class.
        position = source.index("    @property\n    def generic_rows(self):", source.index(class_anchor))
        addition = '    def get_buy_menu_unit_input_row_num(self, pipeline, unit):\n        # Output row ownership is defined by GestaltGraphics, not unit indices.\n        return sum(\n            self.get_output_row_count_for_unit(previous_unit)\n            for previous_unit in pipeline.consist.units[: pipeline.consist.units.index(unit)]\n        )\n\n'
        source = source[:position] + addition + source[position:]
    GESTALT.write_text(source)
    print("Step 001: strategy purchase-row map available")

if __name__ == "__main__":
    main()
