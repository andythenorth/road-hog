from road_vehicle import LogHEQSConsist, DieselVehicleUnit

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="LogHEQS",
        model_id="buff_log",
        base_numeric_id=110,
        name="Buff",
        power=550,
        speed=60,
        gen=4,
    )

    model_def.add_unit_def(
        unit_cls_name="DieselVehicleUnit",
        # capacity=40,
        vehicle_length=7,
    )

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit",
        # capacity=35,
        vehicle_length=8,
    )

    result.append(model_def)
    return result
