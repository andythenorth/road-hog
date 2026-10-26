from road_vehicle.model_def import ModelDef


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="BoxTruck",
        model_id="runwell_box",
        base_numeric_id=890,
        name="Runwell",
        gen=2,
    )

    model_def.add_unit_def(unit_cls_name="SteamCaboverSemiTractorTruckGen2A")

    model_def.add_unit_def(unit_cls_name="RoadVehicleUnit", vehicle_length=5)

    result.append(model_def)
    return result
