from road_vehicle import LogHEQSConsist, DieselVehicleUnit

from road_vehicle.model_def import ModelDef
# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(schema_name='LogHEQS', 
        model_id="knockdown_log",
        base_numeric_id=250,
        name="Knockdown",
        power=250,  # custom power
        speed=50,
        gen=3,
    )

    model_def.add_unit_def(
        base_platform=None,  # no base platform by design currently
        unit_cls_name='DieselVehicleUnit',
        vehicle_length=7,
    )

    model_def.add_unit_def(unit_cls_name='RoadVehicleUnit', 
        base_platform=None, vehicle_length=6  # no base platform by design currently
    )

    return [model_def]
