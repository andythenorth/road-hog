from road_vehicle import LogHEQSConsist, SteamVehicleUnit

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(
        schema_name="LogHEQS",
        model_id="trefell_log",
        base_numeric_id=480,
        name="Trefell",
        power=100,  # custom power
        gen=3,
    )

    model_def.add_unit_def(
        base_platform=None,  # no base platform by design currently
        unit_cls_name="SteamVehicleUnit",
        capacity=0,
        vehicle_length=4,
        effects=["EFFECT_SPRITE_STEAM, -5, 0, 12"],
        always_use_same_spriterow=True,
    )

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit",
        base_platform=None,
        vehicle_length=6,  # no base platform by design currently
    )

    return [model_def]
