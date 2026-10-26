from road_vehicle.model_def import ModelDef


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="TankerFeldbahn",
        model_id="hopping_pipe_tanker",
        base_numeric_id=1140,
        name="Hopping Pipe",
        gen=2,
    )

    model_def.add_unit_def(unit_cls_name="SteamEngineFeldbahnGen2A")

    model_def.add_unit_def(unit_cls_name="WagonFeldbahnA", repeat=5)

    result.append(model_def)
    return result
