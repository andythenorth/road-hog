from road_vehicle import TankerFeldbahnConsist
from base_platforms.feldbahn import DieselEngineFeldbahnGen3B, WagonFeldbahnA

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(
        schema_name="TankerFeldbahn",
        model_id="redoil_tanker",
        base_numeric_id=1120,
        name="Redoil",
        gen=3,
    )

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit", base_platform=DieselEngineFeldbahnGen3B
    )

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit", base_platform=WagonFeldbahnA, repeat=12
    )

    return [model_def]
