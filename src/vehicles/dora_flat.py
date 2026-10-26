from road_vehicle import FlatFeldbahnConsist

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(
        schema_name="FlatFeldbahn",
        model_id="dora_flat",
        base_numeric_id=1070,
        name="Dora",
        gen=3,
    )

    model_def.add_unit_def(
        unit_cls_name="DieselEngineFeldbahnGen3B"
    )

    model_def.add_unit_def(
        unit_cls_name="WagonFeldbahnA", repeat=12
    )

    return [model_def]
