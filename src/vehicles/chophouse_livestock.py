from road_vehicle.model_def import ModelDef


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="LivestockFeldbahn",
        model_id="chophouse_livestock",
        base_numeric_id=1190,
        name="Chophouse",
        gen=2,
    )

    model_def.add_unit_def(unit_cls_name="SteamEngineFeldbahnGen2B")

    model_def.add_unit_def(unit_cls_name="WagonFeldbahnA", repeat=12)

    result.append(model_def)
    return result
