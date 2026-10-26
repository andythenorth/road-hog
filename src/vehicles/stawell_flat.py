from road_vehicle import FlatFeldbahnConsist

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(
        schema_name="FlatFeldbahn",
        model_id="stawell_flat",
        base_numeric_id=1050,
        name="Stawell",
        gen=2,
    )

    model_def.add_unit_def(
        unit_cls_name="SteamEngineFeldbahnGen2A"
    )

    model_def.add_unit_def(
        unit_cls_name="WagonFeldbahnA", repeat=5
    )

    return [model_def]
