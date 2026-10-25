from road_vehicle import DumpHEQSConsist
from base_platforms.heqs import DieselConventionalCabSemiTractorHaulerGen3A

from road_vehicle.model_def import ModelDef
# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(schema_name='DumpHEQS', 
        model_id="broadrock_dump",
        base_numeric_id=100,
        name="Broadrock",
        power=400,
        speed=40,  # dibbled up above RL for game balance
        # CABBAGE type_base_running_cost_points=20,  # dibble running costs for game balance
        gen=3,
        intro_year_offset=-3,
    )  # introduce earlier than gen epoch by design

    model_def.add_unit_def(unit_cls_name='RoadVehicleUnit', base_platform=DieselConventionalCabSemiTractorHaulerGen3A)

    model_def.add_unit_def(unit_cls_name='RoadVehicleUnit', 
        base_platform=None,
        # capacity=55,  # much bigger is not much better here
        vehicle_length=6,
    )

    return [model_def]
