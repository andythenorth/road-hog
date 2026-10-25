from road_vehicle import FlatFeldbahnConsist
from base_platforms.feldbahn import SteamEngineFeldbahnGen2B, WagonFeldbahnA

from road_vehicle.model_def import ModelDef
# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(schema_name='FlatFeldbahn', 
        model_id="newbiggin_flat",
        base_numeric_id=1110,
        name="Newbiggin",
        gen=2,
    )

    model_def.add_unit_def(unit_cls_name='RoadVehicleUnit', base_platform=SteamEngineFeldbahnGen2B)

    model_def.add_unit_def(unit_cls_name='RoadVehicleUnit', base_platform=WagonFeldbahnA, repeat=12)

    return [model_def]
