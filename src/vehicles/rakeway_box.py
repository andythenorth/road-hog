from road_vehicle.model_def import ModelDef


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="BoxTram",
        model_id="rakeway_box",
        base_numeric_id=870,
        name="Rakeway",
        gen=2,
    )

    model_def.add_unit_def(unit_cls_name="ElectricMotorTram3", repeat=2)

    result.append(model_def)
    return result
