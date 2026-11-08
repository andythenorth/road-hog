"""Move visible-cargo compositor row types to the Iron Horse strategy interface."""

# CABBAGE: after Step 018 renames the strategy/template, earlier migration scripts
# are historical steps and must not reapply transformations to the old contracts.
from pathlib import Path as _visible_cargo_migration_path
if (
    _visible_cargo_migration_path("src/templates/vehicle_with_precomposited_cargo.pynml").is_file()
    and not _visible_cargo_migration_path("src/templates/vehicle_with_visible_cargo.pynml").exists()
    and "class GestaltGraphicsPrecompositedCargo"
    in _visible_cargo_migration_path("src/gestalt_graphics/gestalt_graphics.py").read_text(encoding="utf-8")
):
    print("Earlier visible-cargo step superseded by Step 018 rename")
    raise SystemExit(0)


from pathlib import Path
import ast

STRATEGY = Path("src/gestalt_graphics/gestalt_graphics.py")
PIPELINE = Path("src/gestalt_graphics/pipelines.py")

METHOD = '''    def get_spriterow_types_for_units(self, units):
        result = []
        for unit in units:
            if unit.always_use_same_spriterow:
                # CABBAGE: Road Hog fixed-row articulated units have no equivalent
                # in the copied Iron Horse precomposited-cargo row-type contract.
                result.append(["always_use_same_spriterow"])
            else:
                result.append(self.get_output_row_types())
        return result

'''

OLD = '''                if (
                    spriterow_type == "always_use_same_spriterow"
                    or spriterow_type == "empty"
                ):
'''
NEW = '''                if spriterow_type in (
                    "always_use_same_spriterow",
                    "empty",
                    "empty_vehicle_body",
                ):
'''


def main():
    for path in (STRATEGY, PIPELINE):
        if not path.is_file():
            raise SystemExit(f"Run from repository root: missing {path}")
    a = STRATEGY.read_text(encoding="utf-8")
    b = PIPELINE.read_text(encoding="utf-8")
    marker = "class GestaltGraphicsVisibleCargo(GestaltGraphics):"
    if a.count(marker) != 1:
        raise RuntimeError("Visible-cargo class not uniquely found")
    prefix, visible = a.split(marker, 1)
    # Only inspect the subclass, not its base class.
    if METHOD not in visible:
        if "    def get_spriterow_types_for_units(self, units):" in visible.split("class GestaltGraphicsLiveryOnly", 1)[0]:
            raise RuntimeError("Unexpected existing visible-cargo method")
        anchor = "    def get_output_row_types(self):"
        if visible.count(anchor) != 1:
            raise RuntimeError("Expected visible-cargo row-type method once")
        visible = visible.replace(anchor, METHOD + anchor, 1)
        a = prefix + marker + visible
    if OLD in b:
        if b.count(OLD) != 1:
            raise RuntimeError("Ambiguous compositor dispatch")
        b = b.replace(OLD, NEW, 1)
    elif NEW not in b:
        raise RuntimeError("Unexpected compositor dispatch")
    for path, content in ((STRATEGY, a), (PIPELINE, b)):
        ast.parse(content, filename=str(path))
    for path, content in ((STRATEGY, a), (PIPELINE, b)):
        if content != path.read_text(encoding="utf-8"):
            path.write_text(content, encoding="utf-8")
            print(f"Updated {path}")
    print("Step 012: visible-cargo compositor uses Iron Horse row-type naming")


if __name__ == "__main__":
    main()
