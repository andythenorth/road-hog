from road_vehicle import DumpFeldbahnConsist

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(
        schema_name="DumpFeldbahn",
        model_id="jumbo_dump",
        base_numeric_id=1080,
        name="Jumbo",
        gen=2,
    )

    model_def.add_unit_def(
        unit_cls_name="SteamEngineFeldbahnGen2B"
    )

    model_def.add_unit_def(
        unit_cls_name="WagonFeldbahnA", repeat=12
    )  # 12 * 3 = 36, then +4 for engine = 40, 2.5 tiles,  integer tile lengths  are not needed for RVs

    return [model_def]
