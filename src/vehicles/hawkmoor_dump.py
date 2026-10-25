from road_vehicle import DumpTramConsist
from base_platforms.trams import ElectricMotorTram3

from road_vehicle.model_def import ModelDef
# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(schema_name='DumpTram', 
        model_id="hawkmoor_dump",
        base_numeric_id=760,
        name="Hawkmoor",
        gen=2,
        intro_year_offset=2,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(unit_cls_name='RoadVehicleUnit', base_platform=ElectricMotorTram3, repeat=2)

    return [model_def]
