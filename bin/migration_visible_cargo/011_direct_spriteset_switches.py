"""Use direct spritesets in visible-cargo loading switches (Iron Horse pattern)."""

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


TEMPLATE = Path("src/templates/vehicle_with_visible_cargo.pynml")


def main():
    source = TEMPLATE.read_text(encoding="utf-8")
    old_groups = """    spritegroup ${unit.id}_sg_empty_${cargo_variant_num} {
        loaded:  [
            ${unit.id}_ss_empty,
        ];
        loading: [
            ${unit.id}_ss_empty,
        ];
    }
    spritegroup ${unit.id}_sg_loading_${cargo_variant_num} {
        loaded:  [
            ${unit.id}_ss_loading_${cargo_variant_num},
        ];
        loading: [
            ${unit.id}_ss_loading_${cargo_variant_num},
        ];
    }
    spritegroup ${unit.id}_sg_loaded_${cargo_variant_num} {
        loaded:  [
            ${unit.id}_ss_loaded_${cargo_variant_num},
        ];
        loading: [
            ${unit.id}_ss_loaded_${cargo_variant_num},
        ];
    }

"""
    old_returns = (
        "0..24: return ${unit.id}_sg_empty_${cargo_variant_num};",
        "25..90: return ${unit.id}_sg_loading_${cargo_variant_num};",
        "return ${unit.id}_sg_loaded_${cargo_variant_num};",
    )
    new_returns = (
        "0..24: return ${unit.id}_ss_empty;",
        "25..90: return ${unit.id}_ss_loading_${cargo_variant_num};",
        "return ${unit.id}_ss_loaded_${cargo_variant_num};",
    )
    if old_groups in source:
        for old, new in zip(old_returns, new_returns):
            if source.count(old) != 1:
                raise ValueError(f"Expected exactly one load-state return: {old}")
            source = source.replace(old, new)
        source = source.replace(old_groups, "", 1)
        TEMPLATE.write_text(source, encoding="utf-8")
        print("Step 011: direct spriteset loading switches applied")
    elif all(new in source for new in new_returns) and not any(
        old in source for old in old_returns
    ) and "spritegroup ${unit.id}_sg_" not in source:
        print("Step 011: already applied")
    else:
        raise ValueError("Unexpected visible-cargo template; refusing to modify")


if __name__ == "__main__":
    main()
