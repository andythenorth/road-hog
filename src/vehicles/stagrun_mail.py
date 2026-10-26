from road_vehicle.model_def import ModelDef


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="MailTram",
        model_id="stagrun_mail",
        base_numeric_id=840,
        name="Stagrun",
        power=360,  # custom power
        gen=3,
        intro_year_offset=2,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(
        unit_cls_name="ElectricVehicleUnit",
        vehicle_length=4,
        repeat=2,
    )

    result.append(model_def)
    return result
