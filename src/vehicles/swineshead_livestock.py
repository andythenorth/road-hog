from road_vehicle import LivestockTruckConsist
from base_platforms.trucks import DieselCaboverRigidTruckGen4B

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(
        schema_name="LivestockTruck",
        model_id="swineshead_livestock",
        base_numeric_id=440,
        name="Swineshead",
        gen=4,
        intro_year_offset=2,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit",
        base_platform=DieselCaboverRigidTruckGen4B,
        always_use_same_spriterow=True,
    )  # !! because livestock gestalt only has one spriterow - could be done better??

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit", base_platform=None, vehicle_length=4
    )

    return [model_def]
