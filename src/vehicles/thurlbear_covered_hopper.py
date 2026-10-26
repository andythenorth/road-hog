from road_vehicle.model_def import ModelDef


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="CoveredHopperTram",
        model_id="thurlbear_covered_hopper",
        base_numeric_id=460,
        name="Thurlbear",
        gen=3,
    )

    model_def.add_unit_def(unit_cls_name="ElectricMotorTram4", repeat=2)

    result.append(model_def)
    return result
