from road_vehicle import DumpHEQSConsist, DieselVehicleUnit

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="DumpHEQS",
        model_id="witch_hill_dump",
        base_numeric_id=500,
        name="Witch Hill",
        power=900,
        speed=50,  # dibbled up above RL for game balance
        # CABBAGE type_base_running_cost_points=30,  # dibble running costs for game balance
        gen=4,
        intro_year_offset=17,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(
        unit_cls_name="DieselVehicleUnit",
        # capacity=85,  # much bigger is not much better here
        vehicle_length=7,
        effects=[
            "EFFECT_SPRITE_AIRCRAFT_BREAKDOWN_SMOKE, -2, 1, 10",
            "EFFECT_SPRITE_AIRCRAFT_BREAKDOWN_SMOKE, -2, -1, 10",
        ],
    )

    result.append(model_def)
    return result
