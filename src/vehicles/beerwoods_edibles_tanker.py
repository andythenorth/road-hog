from road_vehicle import EdiblesTankerTruckConsist
from base_platforms.trucks import DieselCaboverRigidTruckGen3A

from road_vehicle.model_def import ModelDef
# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(schema_name='EdiblesTankerTruck', 
        model_id="beerwoods_edibles_tanker",
        base_numeric_id=420,
        name="Beerwoods",
        gen=3,
        intro_year_offset=4,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(unit_cls_name='RoadVehicleUnit', base_platform=DieselCaboverRigidTruckGen3A)

    model_def.add_unit_def(unit_cls_name='RoadVehicleUnit', base_platform=None, vehicle_length=4)

    return [model_def]
