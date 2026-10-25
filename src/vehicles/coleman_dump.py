from road_vehicle import DumpTruckConsist
from base_platforms.trucks import SteamCaboverSemiTractorTruckGen2A

from road_vehicle.model_def import ModelDef
# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(schema_name='DumpTruck', 
        model_id="coleman_dump",
        base_numeric_id=910,
        name="Coleman",
        gen=2,
        intro_year_offset=7,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(unit_cls_name='RoadVehicleUnit', base_platform=SteamCaboverSemiTractorTruckGen2A)

    model_def.add_unit_def(unit_cls_name='RoadVehicleUnit', base_platform=None, vehicle_length=5)

    return [model_def]
