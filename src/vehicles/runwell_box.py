from road_vehicle import BoxTruckConsist
from base_platforms.trucks import SteamCaboverSemiTractorTruckGen2A

from road_vehicle.model_def import ModelDef
# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(schema_name='BoxTruck', 
        model_id="runwell_box",
        base_numeric_id=890,
        name="Runwell",
        gen=2,
    )

    model_def.add_unit_def(unit_cls_name='RoadVehicleUnit', base_platform=SteamCaboverSemiTractorTruckGen2A)

    model_def.add_unit_def(unit_cls_name='RoadVehicleUnit', base_platform=None, vehicle_length=5)

    return [model_def]
