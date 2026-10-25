from road_vehicle import RefrigeratedTruckConsist
from base_platforms.trucks import DieselCaboverSemiTractorTruckGen5A

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(
        schema_name="RefrigeratedTruck",
        model_id="coldfall_refrigerated",
        base_numeric_id=150,
        name="Coldfall",
        gen=5,
        intro_year_offset=1,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit",
        base_platform=DieselCaboverSemiTractorTruckGen5A,
    )

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit", base_platform=None, vehicle_length=8
    )

    return [model_def]
