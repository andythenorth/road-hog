from road_vehicle import BoxFeldbahnConsist

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(
        schema_name="BoxFeldbahn",
        model_id="ingleby_box",
        base_numeric_id=1000,
        name="Ingleby",
        gen=2,
    )

    model_def.add_unit_def(
        unit_cls_name="SteamEngineFeldbahnGen2A"
    )

    model_def.add_unit_def(
        unit_cls_name="WagonFeldbahnA", repeat=5
    )

    return [model_def]
