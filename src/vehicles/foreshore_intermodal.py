from road_vehicle.model_def import ModelDef


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="IntermodalHauler",
        model_id="foreshore",
        base_numeric_id=970,
        name="Foreshore",
        power=950,
        gen=4,
        intro_date=1959,
    )

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit", vehicle_length=7
    )  # capacity=50,

    result.append(model_def)
    return result
