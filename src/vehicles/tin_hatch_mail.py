from road_vehicle import MailTramConsist, SteamVehicleUnit

from road_vehicle.model_def import ModelDef
# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(schema_name='MailTram', 
        model_id="tin_hatch_mail",
        base_numeric_id=820,
        name="Tin Hatch",
        power=120,  # custom power
        gen=1,
    )

    model_def.add_unit_def(
        base_platform=None,  # mail trams have no base platform by design currently
        unit_cls_name='SteamVehicleUnit',
        capacity=0,
        vehicle_length=3,
        effects=["EFFECT_SPRITE_STEAM, -3, 0, 12"],
        always_use_same_spriterow=True,
    )

    model_def.add_unit_def(unit_cls_name='RoadVehicleUnit', 
        base_platform=None, vehicle_length=5  # no base platform by design currently
    )

    return [model_def]
