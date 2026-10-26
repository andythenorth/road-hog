from road_vehicle.model_def import ModelDef


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="MailTruck",
        model_id="brass_monkey_mail",
        base_numeric_id=570,
        name="Brass Monkey",
        power=140,
        speed=55,
        gen=3,
        intro_year_offset=1,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(
        unit_cls_name="DieselVehicleUnit",
        vehicle_length=6,
    )

    result.append(model_def)
    return result
