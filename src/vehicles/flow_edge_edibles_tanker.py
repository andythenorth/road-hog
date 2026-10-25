from road_vehicle import EdiblesTankerTruckConsist
from base_platforms.trucks import SteamCaboverRigidTruckGen2A

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(
        schema_name="EdiblesTankerTruck",
        model_id="flow_edge_edibles_tanker",
        base_numeric_id=930,
        name="Flow Edge",
        gen=2,
        intro_year_offset=2,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit", base_platform=SteamCaboverRigidTruckGen2A
    )

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit", base_platform=None, vehicle_length=4
    )

    return [model_def]
