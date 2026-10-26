from road_vehicle import DumpTruckConsist

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(
        schema_name="DumpTruck",
        model_id="gravelhead_dump",
        base_numeric_id=580,
        name="Gravelhead",
        power=130,
        gen=4,
        intro_date=1920,
    )

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit",
        vehicle_length=6,
        effect_spawn_model="EFFECT_SPAWN_MODEL_STEAM",
        effects=["EFFECT_SPRITE_STEAM, -3, 0, 12"],
    )

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit", vehicle_length=5
    )

    return [model_def]
