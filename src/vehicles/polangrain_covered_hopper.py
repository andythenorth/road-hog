from road_vehicle import CoveredHopperTramConsist
from base_platforms.trams import ElectricMotorTram2

from road_vehicle.model_def import ModelDef
# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(schema_name='CoveredHopperTram', 
        model_id="polangrain_covered_hopper",
        base_numeric_id=790,
        name="Polangrain",
        gen=2,
    )

    model_def.add_unit_def(unit_cls_name='RoadVehicleUnit', base_platform=ElectricMotorTram2, repeat=2)

    return [model_def]
