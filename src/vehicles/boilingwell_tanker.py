from road_vehicle.model_def import ModelDef


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="TankerTruck",
        model_id="boilingwell_tanker",
        base_numeric_id=920,
        name="Boilingwell",
        gen=2,
        intro_year_offset=5,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(unit_cls_name="SteamCaboverSemiTractorTruckGen2A")

    model_def.add_unit_def(unit_cls_name="RoadVehicleUnit", vehicle_length=5)

    result.append(model_def)
    return result
