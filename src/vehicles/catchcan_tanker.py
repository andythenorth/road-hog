from road_vehicle.model_def import ModelDef


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="TankerTram",
        model_id="catchcan_tanker",
        base_numeric_id=810,
        name="Catchcan",
        gen=2,
        intro_year_offset=2,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(unit_cls_name="ElectricMotorTram3", repeat=2)

    result.append(model_def)
    return result
