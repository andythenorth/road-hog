from road_vehicle.model_def import ModelDef


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="MetalHEQSBase",
        model_id="steeraway_metal",
        base_numeric_id=520,
        name="Steeraway",
        power=500,
        speed=45,
        gen=3,
        intro_year_offset=10,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(
        unit_cls_name="DieselVehicleUnit",
        capacity=0,
        vehicle_length=6,
    )

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit",
        # capacity=50,
        vehicle_length=7,
        repeat=2,
    )

    result.append(model_def)
    return result
