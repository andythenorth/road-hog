#!/usr/bin/env python3
"""Keep Road Hog's pipeline row contract explicit until its real migration."""

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


import ast
from pathlib import Path

TARGET = Path("src/gestalt_graphics/pipelines.py")
CLASS_NAME = "ExtendSpriterowsForCompositedSpritesPipeline"
LEGACY_CALL = "consist.get_spriterows_for_consist_or_subpart(consist.unique_units)"
OLD_SHIM_CALL = "self.get_spriterow_types_for_model()"
NEW_CALL = "self.get_legacy_road_hog_spriterows_for_consist(consist)"
OLD_METHOD = '''    def get_spriterow_types_for_model(self):
        # CABBAGE: replace Road Hog row descriptors with Iron Horse GestaltGraphics row types.
        return self.example_model_variant.get_spriterows_for_consist_or_subpart(
            self.example_model_variant.unique_units
        )
'''
NEW_METHOD = '''    def get_legacy_road_hog_spriterows_for_consist(self, legacy_consist):
        # CABBAGE: temporary Road Hog row-descriptor shim; replace with Iron Horse GestaltGraphics row types.
        return legacy_consist.get_spriterows_for_consist_or_subpart(
            legacy_consist.unique_units
        )
'''
BAD_ALIAS = "        self.example_model_variant = consist\n"


def main():
    if not TARGET.is_file():
        raise SystemExit(f"Run from repository root: missing {TARGET}")

    original = TARGET.read_text(encoding="utf-8")
    source = original
    tree = ast.parse(source)
    cls = next(
        (
            node
            for node in tree.body
            if isinstance(node, ast.ClassDef) and node.name == CLASS_NAME
        ),
        None,
    )
    if cls is None:
        raise RuntimeError(f"Missing {CLASS_NAME}")

    methods = {node.name for node in cls.body if isinstance(node, ast.FunctionDef)}
    if "get_legacy_road_hog_spriterows_for_consist" in methods:
        if NEW_CALL not in source or BAD_ALIAS in source:
            raise RuntimeError("Incomplete existing Step 4; refusing to continue")
        print(f"Already migrated: {TARGET}")
        return

    if "get_spriterow_types_for_model" in methods and "get_spriterow_types_for_units" in (Path("src/gestalt_graphics/gestalt_graphics.py")).read_text():
        print("Step 004: superseded by Step 010")
        return
    if "get_spriterow_types_for_model" in methods:
        if source.count(OLD_METHOD) != 1 or source.count(OLD_SHIM_CALL) != 1:
            raise RuntimeError("Unexpected prior Step 4 implementation")
        source = source.replace(OLD_METHOD, NEW_METHOD, 1)
        source = source.replace(OLD_SHIM_CALL, NEW_CALL, 1)
        if source.count(BAD_ALIAS) != 1:
            raise RuntimeError("Expected exactly one incorrect compatibility alias")
        source = source.replace(BAD_ALIAS, "", 1)
    else:
        if source.count(LEGACY_CALL) != 1:
            raise RuntimeError("Unexpected legacy row enumeration call")
        lines = source.splitlines(keepends=True)
        lines.insert(cls.body[0].lineno - 1, NEW_METHOD + "\n")
        source = "".join(lines).replace(LEGACY_CALL, NEW_CALL, 1)

    ast.parse(source)
    TARGET.write_text(source, encoding="utf-8")
    print(f"Migrated legacy pipeline boundary: {TARGET}")


if __name__ == "__main__":
    main()
