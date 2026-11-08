#!/usr/bin/env python3
# Step 008b: render uncalled road runtime definitions.
from pathlib import Path
import sys
ROOT = Path.cwd()
TEMPLATES = ROOT / "src/templates"
RENDERER = ROOT / "src/render_nml.py"
SOURCE = Path(__file__).with_name("procedures_wagon_recolour_strategies_road.pynml")
TARGET = TEMPLATES / SOURCE.name

def replace_exact(path, old, new):
    content = path.read_text()
    if new in content:
        return False
    if content.count(old) != 1:
        raise RuntimeError(f"Expected one insertion point in {path}, got {content.count(old)}")
    path.write_text(content.replace(old, new))
    return True

def main():
    if not (TEMPLATES / "alt_vars_random_bits_road.pynml").exists():
        raise RuntimeError("008 foundations missing: alt_vars_random_bits_road.pynml")
    if not (TEMPLATES / "recolour_sprites.pynml").exists():
        raise RuntimeError("008 foundations missing: recolour_sprites.pynml")
    if TARGET.exists():
        if TARGET.read_bytes() != SOURCE.read_bytes():
            raise RuntimeError("Existing road procedures template differs; refusing overwrite")
    else:
        TARGET.write_bytes(SOURCE.read_bytes())
    old = 'header_items = ["header", "cargo_table", "roadtypes_tramtypes", "recolour_sprites"]'
    new = 'header_items = ["header", "cargo_table", "roadtypes_tramtypes", "recolour_sprites", "alt_vars_random_bits_road", "procedures_wagon_recolour_strategies_road"]'
    replace_exact(RENDERER,old,new)
    old = '''            git_info=git_info,
'''
    new = '''            git_info=git_info,
            # CABBAGE352: procedure rendering data, with no vehicle callers yet.
            livery_supplier=runtime_recolour_livery_supplier(),
'''
    replace_exact(RENDERER,old,new)
    old = 'def render_header_item_nml(header_item, roster, consists, graphics_path):'
    new = '''def runtime_recolour_livery_supplier():
    # CABBAGE352: keep IH livery ordering/serialization for uncalled switches.
    from road_vehicle.livery import LiverySupplier

    supplier = LiverySupplier()
    for name, spec in global_constants.freight_wagon_liveries.items():
        supplier.add_livery(name, is_freight_wagon_livery=True, **spec)
    return supplier


def render_header_item_nml(header_item, roster, consists, graphics_path):'''
    replace_exact(RENDERER,old,new)
    print("008b runtime procedure definitions rendered (no callers)")

if __name__ == "__main__":
    main()
