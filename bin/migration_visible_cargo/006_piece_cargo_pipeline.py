#!/usr/bin/env python3
"""Step 006: use Iron Horse's direct piece-cargo iteration; retire legacy map."""

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

PIPELINE = Path("src/gestalt_graphics/pipelines.py")
GESTALT = Path("src/gestalt_graphics/gestalt_graphics.py")
OLD_LOOP = """        # !! convert to use piece_vehicle_type_to_sprites_maps per Iron Horse ??
        for (
            cargo_labels,
            cargo_filenames,
        ) in self.consist.gestalt_graphics.piece_cargo_maps:
            for cargo_filename in cargo_filenames:
"""
NEW_LOOP = """        for cargo_filename in polar_fox.constants.piece_vehicle_type_to_sprites_maps[
            self.consist.gestalt_graphics.piece_type
        ]:
"""


def locate_method(source, class_name, method_name):
    tree = ast.parse(source)
    cls = next(
        (node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == class_name),
        None,
    )
    if cls is None:
        raise RuntimeError(f"Missing class {class_name}")
    return next(
        (node for node in cls.body if isinstance(node, ast.FunctionDef) and node.name == method_name),
        None,
    )


def migrate_pipeline(source):
    if OLD_LOOP in source:
        if source.count(OLD_LOOP) != 1:
            raise RuntimeError("Unexpected duplicate legacy cargo loops")
        lines = source.replace(OLD_LOOP, NEW_LOOP, 1).splitlines(keepends=True)
        # The old loop nested cargo composition one additional level.
        start = next(i for i, line in enumerate(lines) if line.startswith(NEW_LOOP.splitlines()[0]))
        method = locate_method(source, "ExtendSpriterowsForCompositedSpritesPipeline", "render")
        if method is None:
            raise RuntimeError("Missing compositor render boundary")
        end = next(i for i in range(start + 1, len(lines)) if lines[i].startswith("    def render(self, consist,"))
        if not any("cargo_sprite_num" in line for line in lines[start:end]):
            raise RuntimeError("Unexpected cargo compositor block")
        for i in range(start + len(NEW_LOOP.splitlines()), end):
            if lines[i].strip():
                if not lines[i].startswith("    "):
                    raise RuntimeError("Unexpected cargo block indentation")
                lines[i] = lines[i][4:]
        result = "".join(lines)
        ast.parse(result)
        return result
    if NEW_LOOP in source and "piece_cargo_maps" not in source:
        return source
    raise RuntimeError("Unknown piece cargo compositor state")


def migrate_gestalt(source):
    method = locate_method(source, "GestaltGraphicsVisibleCargo", "piece_cargo_maps")
    if method is None:
        if "def piece_cargo_maps(" in source:
            raise RuntimeError("Legacy property exists outside expected class")
        return source
    start = min([method.lineno] + [d.lineno for d in method.decorator_list]) - 1
    end = method.end_lineno
    lines = source.splitlines(keepends=True)
    # A Step 005 CABBAGE marker appears inside this property's body and is retired with it.
    lines[start:end] = []
    result = "".join(lines)
    ast.parse(result)
    if "self.piece_cargo_maps" in result:
        # Row-count calculation still refers to the legacy property, so replace it
        # with the same count read from Iron Horse's ordered sprite filename map.
        old = "2 * sum([len(cargo_map[1]) for cargo_map in self.piece_cargo_maps])"
        new = "2 * len(polar_fox.constants.piece_vehicle_type_to_sprites_maps[self.piece_type])"
        if result.count(old) != 1:
            raise RuntimeError("Unexpected row-count dependency")
        result = result.replace(old, new, 1)
    if "piece_cargo_maps" in result:
        raise RuntimeError("Unretired reference to piece_cargo_maps")
    ast.parse(result)
    return result


def main():
    if not PIPELINE.is_file() or not GESTALT.is_file():
        raise SystemExit("Run from the Road Hog repository root")
    original_pipeline = PIPELINE.read_text(encoding="utf-8")
    original_gestalt = GESTALT.read_text(encoding="utf-8")
    pipeline = migrate_pipeline(original_pipeline)
    gestalt = migrate_gestalt(original_gestalt)
    ast.parse(pipeline)
    ast.parse(gestalt)
    if pipeline != original_pipeline:
        PIPELINE.write_text(pipeline, encoding="utf-8")
    if gestalt != original_gestalt:
        GESTALT.write_text(gestalt, encoding="utf-8")
    print("Step 006: direct piece-cargo iteration and legacy property retirement complete")


if __name__ == "__main__":
    main()
