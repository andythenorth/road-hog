from road_vehicle import TankerTruckConsist
from base_platforms.trucks import DieselCaboverSemiTractorTruckGen5A

from road_vehicle.model_def import ModelDef
# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(schema_name='TankerTruck', 
        model_id="cloud_hill_tanker",
        base_numeric_id=130,
        name="Cloud Hill",
        gen=5,
        intro_year_offset=4,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(unit_cls_name='RoadVehicleUnit', base_platform=DieselCaboverSemiTractorTruckGen5A)

    model_def.add_unit_def(unit_cls_name='RoadVehicleUnit', base_platform=None, vehicle_length=7)

    return [model_def]
