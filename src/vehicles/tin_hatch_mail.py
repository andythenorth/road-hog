from road_vehicle.model_def import ModelDef


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="MailTram",
        model_id="tin_hatch_mail",
        base_numeric_id=820,
        name="Tin Hatch",
        power=120,  # custom power
        gen=1,
    )

    model_def.add_unit_def(
        unit_cls_name="SteamVehicleUnit",
        capacity=0,
        vehicle_length=3,
        effects=["EFFECT_SPRITE_STEAM, -3, 0, 12"],
        always_use_same_spriterow=True,
    )

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit",
        vehicle_length=5,  # no base platform by design currently
    )

    result.append(model_def)
    return result
