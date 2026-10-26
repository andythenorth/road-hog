from road_vehicle.model_def import ModelDef


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="OpenTram",
        model_id="buildwas_open",
        base_numeric_id=120,
        name="Buildwas",
        gen=1,
    )

    model_def.add_unit_def(unit_cls_name="SteamEngineTram1")

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit",
        vehicle_length=4,
        cargo_length=4,
        repeat=3,
    )

    result.append(model_def)
    return result
