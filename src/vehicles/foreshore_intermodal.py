from road_vehicle import IntermodalHaulerConsist

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(
        schema_name="IntermodalHauler",
        model_id="foreshore",
        base_numeric_id=970,
        name="Foreshore",
        power=950,
        gen=4,
        intro_date=1959,
    )

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit", vehicle_length=7
    )  # capacity=50,

    return [model_def]
