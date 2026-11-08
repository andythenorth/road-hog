#!/usr/bin/env python3
"""Move Road Hog output-row ownership to GestaltGraphics.

Keep the compositor's tuple-based row descriptors until the later Iron Horse
pipeline cutover. The NML enumerator now consumes the same row-group contract.
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


import ast
from pathlib import Path

STRATEGY_PATH = Path("src/gestalt_graphics/gestalt_graphics.py")
PIPELINE_PATH = Path("src/gestalt_graphics/pipelines.py")
SCHEMA_PATH = Path("src/road_vehicle/schemas.py")

OLD_SCHEMA_METHOD = '''    # CABBAGE MIGRATION SHIM: existing graphics pipelines use legacy sprite-row counts.
    # CABBAGE Keep the original row-count semantics for incomplete sprites and cargo.
    def get_spriterows_for_consist_or_subpart(self, units):
        result = []
        for unit in units:
            unit_rows = []
            if unit.always_use_same_spriterow:
                unit_rows.append(("always_use_same_spriterow", 1))
            else:
                unit_rows.extend(self.gestalt_graphics.get_output_row_counts_by_type())
            result.append(unit_rows)
        return result
'''

NEW_STRATEGY_METHOD = '''    def get_legacy_road_hog_output_row_groups(self, units):
        # CABBAGE: temporary tuple row descriptors for the Road Hog compositor;
        # replace with Iron Horse row-type contracts during pipeline cutover.
        result = []
        for unit in units:
            unit_rows = []
            if unit.always_use_same_spriterow:
                unit_rows.append(("always_use_same_spriterow", 1))
            else:
                unit_rows.extend(self.get_output_row_counts_by_type())
            result.append(unit_rows)
        return result

'''

OLD_PIPELINE_METHOD = '''    def get_legacy_road_hog_spriterows_for_consist(self, legacy_consist):
        # CABBAGE: temporary Road Hog row-descriptor shim; replace with Iron Horse GestaltGraphics row types.
        return legacy_consist.get_spriterows_for_consist_or_subpart(
            legacy_consist.unique_units
        )
'''

NEW_PIPELINE_METHOD = '''    def get_legacy_road_hog_spriterows_for_consist(self, legacy_consist):
        # CABBAGE: the pipeline still consumes tuple descriptors rather than
        # Iron Horse row types; the graphics strategy now owns their selection.
        return legacy_consist.gestalt_graphics.get_legacy_road_hog_output_row_groups(
            legacy_consist.unique_units
        )
'''

OLD_OFFSET = '''        preceding_output_rows = 0
        for preceding_unit in unit.model_variant.units:
            if preceding_unit is unit:
                break
            if preceding_unit.always_use_same_spriterow:
                preceding_output_rows += 1
            else:
                preceding_output_rows += sum(
                    row_count
                    for _, row_count in self.get_output_row_counts_by_type()
                )
        else:
            raise ValueError("Unit not found in model variant: " + unit.id)
'''

NEW_OFFSET = '''        preceding_output_rows = 0
        row_groups = self.get_legacy_road_hog_output_row_groups(
            unit.model_variant.units
        )
        for preceding_unit, unit_row_groups in zip(unit.model_variant.units, row_groups):
            if preceding_unit is unit:
                break
            preceding_output_rows += sum(row_count for _, row_count in unit_row_groups)
        else:
            raise ValueError("Unit not found in model variant: " + unit.id)
'''

OLD_OFFSET_COMMENT = '''        # CABBAGE: output grouping still follows the legacy Road Hog compositor;
        # migrate it to Iron Horse's row-type contract with the pipeline.
'''
NEW_OFFSET_COMMENT = '''        # CABBAGE: output offsets still use legacy Road Hog row descriptors;
        # both NML and the compositor now derive them from GestaltGraphics.
'''


def replace_once(source, old, new, label):
    if old in source:
        if source.count(old) != 1:
            raise RuntimeError(f"Ambiguous {label}")
        return source.replace(old, new, 1)
    if new in source:
        return source
    raise RuntimeError(f"Unexpected source layout for {label}; refusing to edit")


def main():
    for path in (STRATEGY_PATH, PIPELINE_PATH, SCHEMA_PATH):
        if not path.is_file():
            raise SystemExit(f"Run from repository root: missing {path}")

    original = {path: path.read_text(encoding="utf-8") for path in (
        STRATEGY_PATH, PIPELINE_PATH, SCHEMA_PATH
    )}
    strategy = original[STRATEGY_PATH]
    anchor = "class GestaltGraphicsVisibleCargo(GestaltGraphics):"
    if NEW_STRATEGY_METHOD not in strategy:
        if strategy.count(anchor) != 1:
            raise RuntimeError("Missing or ambiguous GestaltGraphicsVisibleCargo")
        # Put the method in the shared base: non-visible-cargo strategies may
        # continue producing row groups through get_output_row_counts_by_type.
        # This preserves the old schema method's generic behaviour.
        base_anchor = "class GestaltGraphicsVisibleCargo(GestaltGraphics):"
        strategy = strategy.replace(base_anchor, NEW_STRATEGY_METHOD + "\n" + base_anchor, 1)
    if "preceding_output_rows += self.get_output_row_count_for_unit(" not in strategy:
        strategy = replace_once(strategy, OLD_OFFSET, NEW_OFFSET, "unit output offsets")
        strategy = replace_once(strategy, OLD_OFFSET_COMMENT, NEW_OFFSET_COMMENT, "offset comment")

    if "def get_spriterow_types_for_model(self, model_variant):" in original[PIPELINE_PATH]:
        pipeline = original[PIPELINE_PATH]
    else:
        pipeline = replace_once(
            original[PIPELINE_PATH], OLD_PIPELINE_METHOD, NEW_PIPELINE_METHOD,
            "pipeline row-group caller",
        )
    schema = original[SCHEMA_PATH]
    if OLD_SCHEMA_METHOD in schema:
        schema = schema.replace(OLD_SCHEMA_METHOD, "", 1)
    elif "def get_spriterows_for_consist_or_subpart(self, units):" in schema:
        raise RuntimeError("Unexpected schema legacy row owner")

    changes = {
        STRATEGY_PATH: strategy,
        PIPELINE_PATH: pipeline,
        SCHEMA_PATH: schema,
    }
    # Parse and validate all three files before writing any of them.
    for path, source in changes.items():
        ast.parse(source, filename=str(path))
    for path, source in changes.items():
        if source != original[path]:
            path.write_text(source, encoding="utf-8")
            print(f"Updated {path}")
    print("Step 009: row-group ownership centralised in GestaltGraphics")


if __name__ == "__main__":
    main()
