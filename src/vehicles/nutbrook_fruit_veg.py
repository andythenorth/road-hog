from road_vehicle.model_def import ModelDef


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="FruitVegTram",
        model_id="nutbrook_fruit_veg",
        base_numeric_id=960,
        name="Nutbrook",
        gen=3,
    )

    model_def.add_unit_def(unit_cls_name="ElectricMotorTram4", repeat=2)

    result.append(model_def)
    return result
