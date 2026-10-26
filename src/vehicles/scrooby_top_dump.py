from road_vehicle.model_def import ModelDef


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="DumpTram",
        model_id="scrooby_top_dump",
        base_numeric_id=700,
        name="Scrooby Top",
        gen=1,
        intro_year_offset=10,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(unit_cls_name="SteamEngineTram2")

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit",
        vehicle_length=3,
        repeat=4,
    )

    result.append(model_def)
    return result
