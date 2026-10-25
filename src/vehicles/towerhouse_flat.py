from road_vehicle import FlatbedTruckConsist
from base_platforms.trucks import DieselConventionalCabSemiTractorTruckGen4A

from road_vehicle.model_def import ModelDef
# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(schema_name='FlatbedTruck', 
        model_id="towerhouse_flat",
        base_numeric_id=650,
        name="Towerhouse",
        gen=4,
    )

    model_def.add_unit_def(unit_cls_name='RoadVehicleUnit', base_platform=DieselConventionalCabSemiTractorTruckGen4A)

    model_def.add_unit_def(unit_cls_name='RoadVehicleUnit', 
        base_platform=None, vehicle_length=7, cargo_length=4
    )  # some cargo overlap eh?

    return [model_def]
