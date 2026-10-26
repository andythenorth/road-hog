from road_vehicle.model_def import ModelDef


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="MailTruck",
        model_id="goldmire_mail",
        base_numeric_id=200,
        name="Goldmire",
        power=250,  # custom power
        speed=75,
        gen=4,
        intro_year_offset=1,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(
        unit_cls_name="DieselVehicleUnit",
        vehicle_length=6,
    )

    result.append(model_def)
    return result
