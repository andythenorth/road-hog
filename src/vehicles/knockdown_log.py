from road_vehicle.model_def import ModelDef


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="LogHEQS",
        model_id="knockdown_log",
        base_numeric_id=250,
        name="Knockdown",
        power=250,  # custom power
        speed=50,
        gen=3,
    )

    model_def.add_unit_def(
        unit_cls_name="DieselVehicleUnit",
        vehicle_length=7,
    )

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit",
        vehicle_length=6,  # no base platform by design currently
    )

    result.append(model_def)
    return result
