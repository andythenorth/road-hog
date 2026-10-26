from road_vehicle.model_def import ModelDef


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="MailTram",
        model_id="strongbox_mail",
        base_numeric_id=830,
        name="Strongbox",
        power=480,  # custom power
        gen=4,
        intro_year_offset=1,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(
        unit_cls_name="ElectricVehicleUnit",
        vehicle_length=8,
        effects=["EFFECT_SPRITE_ELECTRIC, 0, 0, 10"],
    )

    result.append(model_def)
    return result
