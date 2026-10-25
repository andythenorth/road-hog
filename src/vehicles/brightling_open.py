from road_vehicle import OpenTramConsist, ElectricVehicleUnit

from road_vehicle.model_def import ModelDef
# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(schema_name='OpenTram', 
        model_id="brightling_open",
        base_numeric_id=90,
        name="Brightling",
        gen=3,
    )

    model_def.add_unit_def(
        base_platform=None,  # no base platform by design currently
        unit_cls_name='ElectricVehicleUnit',
        capacity=0,
        vehicle_length=4,
        always_use_same_spriterow=True,
    )

    model_def.add_unit_def(unit_cls_name='RoadVehicleUnit', 
        base_platform=None,  # no base platform by design currently
        vehicle_length=6,
        cargo_length=3,
        repeat=2,
    )

    return [model_def]
