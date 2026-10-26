"""Replace the first bus schema with the fleet schema."""

import ast
from pathlib import Path


SOURCE = Path("src/road_vehicle/schemas.py")
VEHICLE_MODULES = (
    "highgate_pax.py",
    "leyburn_pax.py",
    "thunder_pax.py",
    "topley_pax.py",
)

REMOVE_COMMENTS = {
    "# CABBAGE MIGRATION SHIM: legacy Consist default; child schemas override as needed.",
    "# CABBAGE Old Road Hog returned 999 here as a shim. Use the real year now;",
    "# check the docs ordering again when we move vehicles with exact intro dates.",
    "# CABBAGE Legacy Consist distinguishes road and tram NML expressions.",
    "# CABBAGE The render entry point is deliberately new-schema only, not a Consist shim.",
    "# CABBAGE Multi-unit / articulated output needs its own legacy parity fixture.",
    "# CABBAGE Power suffix must be supplied by unit integration in Stage 007.",
    "# CABBAGE Fail explicitly rather than silently inventing Diesel/Steam.",
    "# CABBAGE BEGIN GENERATED FLEET SCHEMAS STAGE 005",
    "# CABBAGE END GENERATED FLEET SCHEMAS STAGE 005",
    "# CABBAGE BEGIN SCHEMA BEHAVIOUR STAGE 006",
    "# CABBAGE Dynamic method installation is deliberately NOT used: the definitions",
    "# CABBAGE below are added inside their target class bodies by this installer.",
    "# CABBAGE END SCHEMA BEHAVIOUR STAGE 006",
}
OLD_DOCSTRING = (
    '"""Road-specific schema classes, initially only the bus route is used.\n\n'
    'The catalogue makes model variants. These classes give them Road Hog behaviour.\n'
    'CABBAGE Add more child schemas as the rest of the fleet is converted.\n"""'
)
NEW_DOCSTRING = (
    '"""Road-specific schema classes.\n\n'
    'The catalogue makes model variants. These classes give them Road Hog behaviour.\n"""'
)


def main():
    original = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(original, filename=str(SOURCE))
    lines = original.splitlines(keepends=True)
    deleted = set()
    removed_classes = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name in {"PassengerVehicle", "Bus"}:
            removed_classes.append(node.name)
            deleted.update(range(node.lineno - 1, node.end_lineno))
    if removed_classes and set(removed_classes) != {"PassengerVehicle", "Bus"}:
        raise RuntimeError("Expected both Bus and PassengerVehicle, or neither")

    for index, line in enumerate(lines):
        if line.strip() in REMOVE_COMMENTS:
            deleted.add(index)

    updated = "".join(line for index, line in enumerate(lines) if index not in deleted)
    updated = updated.replace(OLD_DOCSTRING, NEW_DOCSTRING)
    if OLD_DOCSTRING in updated:
        raise RuntimeError("Could not update obsolete module docstring")
    if removed_classes:
        updated = updated.replace("\n\n\n\n\nimport polar_fox", "\n\nimport polar_fox", 1)

    bus_class = """class PaxLocalBus(PaxHaulerLocalConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.base_track_type_name = TrackTypeMixinTruckBusCoach.base_track_type_name
        self.roadveh_flag_tram = TrackTypeMixinTruckBusCoach.roadveh_flag_tram
        self.tractive_effort_coefficient = (
            TrackTypeMixinTruckBusCoach.tractive_effort_coefficient
        )
        self.name_suffix_vehicle_type = (
            TrackTypeMixinTruckBusCoach.name_suffix_vehicle_type
        )
        self._sound_effect = "SOUND_DEPARTURE_OLD_RV_1"
        self.vehicle_role = "bus"

    @property
    def name_type_suffix(self):
        return "STR_NAME_SUFFIX_BUS"


"""
    if "class PaxLocalBus(" not in updated:
        anchor = "class PaxLocalTram(PaxHaulerLocalConsistBase):"
        if updated.count(anchor) != 1:
            raise RuntimeError("Could not find insertion point for PaxLocalBus")
        updated = updated.replace(anchor, bus_class + anchor)

    ast.parse(updated, filename=str(SOURCE))
    replacements = {}
    for name in VEHICLE_MODULES:
        path = Path("src/vehicles") / name
        content = path.read_text(encoding="utf-8")
        if 'schema_name="Bus"' in content:
            replacements[path] = content.replace(
                'schema_name="Bus"', 'schema_name="PaxLocalBus"'
            )
        elif 'schema_name="PaxLocalBus"' not in content:
            raise RuntimeError(f"Unexpected schema in {path}")

    if updated != original:
        SOURCE.write_text(updated, encoding="utf-8")
    for path, content in replacements.items():
        path.write_text(content, encoding="utf-8")
    print(f"{SOURCE}: removed Bus and PassengerVehicle; added PaxLocalBus")
    print(f"Updated {len(replacements)} vehicle schema declarations")


if __name__ == "__main__":
    main()
