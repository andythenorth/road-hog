from road_vehicle import FruitVegTramConsist
from base_platforms.trams import ElectricMotorTram4

from road_vehicle.model_def import ModelDef
# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(schema_name='FruitVegTram', 
        model_id="nutbrook_fruit_veg",
        base_numeric_id=960,
        name="Nutbrook",
        gen=3,
    )

    model_def.add_unit_def(unit_cls_name='RoadVehicleUnit', base_platform=ElectricMotorTram4, repeat=2)

    return [model_def]
