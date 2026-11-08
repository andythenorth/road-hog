#!/usr/bin/env python3
"""Use Iron Horse-style spriteset enumeration in the visible-cargo template.

The original spriteset declarations remain available for custom graphics
strategies without the enumerator. Cargo switches are intentionally unchanged.
"""

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

TARGET = Path("src/templates/vehicle_with_visible_cargo.pynml")
START = '<tal:include metal:use-macro="load: spriteset_templates.pynml" />\n'
END = '\n    spritegroup ${unit.id}_sg_empty_${cargo_variant_num} {'
MARKER = '<tal:enumerated_visible_cargo condition="hasattr(model_variant.gestalt_graphics, \'get_unique_spritesets\')">'

ENUMERATED = '''<tal:enumerated_visible_cargo condition="hasattr(model_variant.gestalt_graphics, 'get_unique_spritesets')">
    <tal:spritesets repeat="spriteset_data model_variant.gestalt_graphics.get_unique_spritesets(unit)">
        spriteset(${unit.id}_ss_${'empty' if spriteset_data[0] == 'empty_unweathered' else spriteset_data[0]}, "${global_constants.graphics_path}${model_variant.model_def.model_id}.png") {
            ${unit.get_spriteset_template_name('unreversed', spriteset_data[1])}
        }
    </tal:spritesets>
</tal:enumerated_visible_cargo>

<tal:legacy_custom_cargo condition="not hasattr(model_variant.gestalt_graphics, 'get_unique_spritesets')">
spriteset(${unit.id}_ss_empty, "${global_constants.graphics_path}${model_variant.model_def.model_id}.png") {
  spriteset_template_${unit.id}(${unit.spriterow_num * 30} + 10)
}
<tal:cargo_variants repeat="cargo_variant_num python:range(model_variant.gestalt_graphics.num_cargo_sprite_variants)">
    spriteset(${unit.id}_ss_loading_${cargo_variant_num}, "${global_constants.graphics_path}${model_variant.model_def.model_id}.png") {
      spriteset_template_${unit.id}(${unit.spriterow_num * 30} + ${cargo_variant_num * 60} + 40)
    }
    spriteset(${unit.id}_ss_loaded_${cargo_variant_num}, "${global_constants.graphics_path}${model_variant.model_def.model_id}.png") {
      spriteset_template_${unit.id}(${unit.spriterow_num * 30} + ${cargo_variant_num * 60} + 70)
    }
</tal:cargo_variants>
</tal:legacy_custom_cargo>

<tal:cargo_variants repeat="cargo_variant_num python:range(model_variant.gestalt_graphics.num_cargo_sprite_variants)">'''


def main():
    if not TARGET.is_file():
        raise SystemExit(f"Run from repository root: missing {TARGET}")
    source = TARGET.read_text(encoding="utf-8")
    if MARKER in source:
        print(f"Already migrated: {TARGET}")
        return
    if not source.startswith(START):
        raise RuntimeError("Unexpected visible-cargo template header; refusing to edit")
    try:
        end = source.index(END)
    except ValueError as exc:
        raise RuntimeError("Original spriteset block not found") from exc
    original = source[len(START) : end]
    if (
        'spriteset(${unit.id}_ss_empty,' not in original
        or 'spriteset(${unit.id}_ss_loaded_${cargo_variant_num}' not in original
        or original.count('<tal:cargo_variants') != 1
    ):
        raise RuntimeError("Unexpected existing spriteset definitions; refusing to edit")
    result = START + '\n' + ENUMERATED + source[end:]
    TARGET.write_text(result, encoding="utf-8")
    print(f"Migrated spriteset declarations in {TARGET}")


if __name__ == "__main__":
    main()
