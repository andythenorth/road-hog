from road_vehicle import OpenFeldbahnConsist

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(
        schema_name="OpenFeldbahn",
        model_id="imperial_open",
        base_numeric_id=1090,
        name="Imperial",
        gen=2,
    )

    model_def.add_unit_def(
        unit_cls_name="SteamEngineFeldbahnGen2B"
    )

    model_def.add_unit_def(
        unit_cls_name="WagonFeldbahnA", repeat=12
    )

    return [model_def]
