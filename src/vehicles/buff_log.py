from road_vehicle.model_def import ModelDef


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="LogHEQS",
        model_id="buff_log",
        base_numeric_id=110,
        name="Buff",
        power=550,
        speed=60,
        gen=4,
    )

    model_def.add_unit_def(
        unit_cls_name="DieselVehicleUnit",
        # capacity=40,
        vehicle_length=7,
    )

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit",
        # capacity=35,
        vehicle_length=8,
    )

    result.append(model_def)
    return result
