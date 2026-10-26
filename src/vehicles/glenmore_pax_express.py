from road_vehicle.model_def import ModelDef

# for each generation, bus and coach variants have same power and intro date
# coaches faster, lower capacity than equivalent bus


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="PaxExpressCoach",
        model_id="glenmore_pax_express",
        base_numeric_id=50,
        name="Glenmore",
        power=160,
        speed=55,
        gen=3,
        intro_year_offset=-4,
    )  # introduce earlier than gen epoch by design

    model_def.add_unit_def(
        unit_cls_name="DieselVehicleUnit",
        vehicle_length=7,
    )

    result.append(model_def)
    return result
