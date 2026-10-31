#!/usr/bin/env python3
"""013: Port Iron Horse ID validation, retaining its implementation verbatim
apart from Road Hog's ``self.consists`` collection name.

Run from repository root. Does not change any vehicle ID declarations.
"""
from pathlib import Path
import ast
import re

IRON_HORSE_METHOD = r'''
    def validate_vehicle_ids(self, numeric_id_defender):
        # has to be explicitly called after all model variants and units are registered to the roster

        # this structure is used to test for duplicate ids
        model_variant_id_counts = Counter(self.consists)
        # we defer collisions until they're all found
        collision_errors = []

        for model_variant in self.consists:
            """
            # pickled test nerfed off as (1) slow (2) mp_logger is now used, which should improve the error output when pickle does fail
            # if model_variant won't pickle, then multiprocessing blows up, catching it here is faster and easier
            try:
                pickle.dumps(model_variant)
            except:
                print("Pickling failed for model_variant:", model_variant.id)
                raise
            """
            if model_variant_id_counts[model_variant.id] > 1:
                raise BaseException(
                    f"Error: vehicle id '{model_variant.id}' is defined more than once - to fix, search src for the duplicate.\n"
                    f"The catalogue for one of them is:"
                    f"{model_variant.catalogue}"
                )
            if len(model_variant.units) == 0:
                raise BaseException(f"Error: {model_variant.id} has no units defined")
            elif len(model_variant.units) == 1:
                if model_variant.base_numeric_id <= global_constants.max_articulated_id:
                    raise BaseException(
                        f"Error: {model_variant.id} with base_numeric_id {model_variant.base_numeric_id} needs a base_numeric_id larger than 16383 "
                        f"as the range below 16383 is reserved for articulated vehicles.\n"
                        f"{model_variant.units}\n"
                        f"Unused IDs might be found in build_logs/id_report.py.log"
                    )
            elif len(model_variant.units) > 1:
                for numeric_id in model_variant.catalogue_entry.unit_numeric_ids:
                    if numeric_id > global_constants.max_articulated_id:
                        raise BaseException(
                            f"Error: {model_variant.id} has a unit variant with numeric_id {numeric_id} which is part of an articulated vehicle "
                            f"and needs a numeric_id smaller than {global_constants.max_articulated_id}.\n"
                            f"Use a lower base_numeric_id in the model_def.\n"
                            f"{model_variant.catalogue.unit_numeric_ids}"
                            f"Unused IDs might be found in build_logs/id_report.py.log"
                        )
            for numeric_id in model_variant.catalogue_entry.unit_numeric_ids:
                if numeric_id % 10 != 0:
                    continue  # only care about block-starting IDs
                if numeric_id in numeric_id_defender:
                    colliding_model_variant = numeric_id_defender[numeric_id]
                    if hasattr(model_variant, "model_id_root"):
                        if (
                            getattr(colliding_model_variant, "model_id_root", None)
                            == model_variant.model_id_root
                            and colliding_model_variant.roster.id
                            != model_variant.roster.id
                        ):
                            continue
                    # Collect all block-starting IDs (multiples of 10) for both variants
                    this_blocks = sorted(
                        {
                            nid
                            for entry in model_variant.catalogue
                            for nid in entry.unit_numeric_ids
                            if nid % 10 == 0
                        }
                    )
                    other_blocks = sorted(
                        {
                            nid
                            for entry in colliding_model_variant.catalogue
                            for nid in entry.unit_numeric_ids
                            if nid % 10 == 0
                        }
                    )
                    collision_errors.append(
                        {
                            "numeric_id": numeric_id,
                            "model_variant": model_variant.id,
                            "collides_with": colliding_model_variant.id,
                            "this_blocks": this_blocks,
                            "other_blocks": other_blocks,
                        }
                    )
                else:
                    numeric_id_defender[numeric_id] = model_variant

        if collision_errors:
            error_msg = [
                "Vehicle ID collisions detected (only multiple-of-10 IDs shown):"
            ]
            for err in collision_errors:
                error_msg.append(
                    f"{err['model_variant']} and {err['collides_with']} share numeric_id {err['numeric_id']}"
                )
                error_msg.append(f"    {err['model_variant']}: {err['this_blocks']}")
                error_msg.append(f"    {err['collides_with']}: {err['other_blocks']}")
                error_msg.append(f"")  # just a spacer
            error_msg.append(
                f"Unused numeric IDs might be found in build_logs/id_report.py.log"
            )
            raise ValueError("\n".join(error_msg))
        # no return value needed

'''

root = Path.cwd()
roster_path = root / "src/roster.py"
entry_path = root / "src/road_hog.py"
report_path = root / "src/id_report.py"

for path in (roster_path, entry_path, report_path):
    if not path.is_file():
        raise SystemExit(f"Missing expected file: {path}")

roster = roster_path.read_text()
entry = entry_path.read_text()
report = report_path.read_text()

# Refuse to overwrite a prior validation migration or an unexpected method.
start = roster.find("    def validate_vehicles(self, numeric_id_defender):")
if start < 0:
    raise SystemExit("Expected original Roster.validate_vehicles() not found; git reset first")
end = roster.find("\n    def ", start + 8)
if end < 0 or "validate_vehicles is nerfed" not in roster[start:end]:
    raise SystemExit("Unexpected Roster validation body; inspect manually")
if re.search(r"^    def validate_vehicle_ids\(", roster, re.M):
    raise SystemExit("validate_vehicle_ids already present")

# Iron Horse's method requires Counter. Keep all other imports unchanged.
if not re.search(r"^from collections import .*\bCounter\b", roster, re.M):
    roster = "from collections import Counter\n" + roster
    # leading import shifts positions of old method
    start = roster.find("    def validate_vehicles(self, numeric_id_defender):")
    end = roster.find("\n    def ", start + 8)

roster = roster[:start] + IRON_HORSE_METHOD + roster[end:]

# Iron Horse manager: dict defender, method name; preserve the other lifecycle.
old = "self.numeric_id_defender = []"
if entry.count(old) != 1:
    raise SystemExit("Expected exactly one list-based numeric_id_defender")
entry = entry.replace(old, "self.numeric_id_defender = {}", 1)
old = "roster.validate_vehicles(self.numeric_id_defender)"
if entry.count(old) != 1:
    raise SystemExit("Expected exactly one old roster validation call")
entry = entry.replace(old, "roster.validate_vehicle_ids(self.numeric_id_defender)", 1)

# Adapt the Iron Horse report's project-name references and call validation.
if "import iron_horse" not in report or "iron_horse.main()" not in report:
    raise SystemExit("Expected unadapted Iron Horse id_report.py; inspect manually")
report = report.replace("import iron_horse", "import road_hog")
report = report.replace("iron_horse.main()", "road_hog.main(validate_vehicle_ids=True)")
report = report.replace("iron_horse.roster_manager", "road_hog.roster_manager")
# Existing function parameter was ignored in copied Iron Horse report.
report = report.replace(
    "if id not in road_hog.roster_manager.numeric_id_defender:",
    "if id not in numeric_id_defender:",
)

for path, content in ((roster_path, roster), (entry_path, entry), (report_path, report)):
    ast.parse(content, filename=str(path))

for path, content in ((roster_path, roster), (entry_path, entry), (report_path, report)):
    path.write_text(content)
    print(f"Updated {path}")
