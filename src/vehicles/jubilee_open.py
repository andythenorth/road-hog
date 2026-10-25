from road_vehicle import OpenFeldbahnConsist
from base_platforms.feldbahn import SteamEngineFeldbahnGen1A, WagonFeldbahnA

from road_vehicle.model_def import ModelDef
# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(schema_name='OpenFeldbahn', 
        model_id="limpet_open", base_numeric_id=220, name="Limpet", gen=2
    )

    model_def.add_unit_def(unit_cls_name='RoadVehicleUnit', base_platform=SteamEngineFeldbahnGen1A)

    model_def.add_unit_def(unit_cls_name='RoadVehicleUnit', base_platform=WagonFeldbahnA, repeat=5)

    return [model_def]
