from road_vehicle.model_def import ModelDef


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="OpenTruck",
        model_id="jinglepot_open",
        base_numeric_id=240,
        name="Jinglepot",
        gen=2,
    )

    model_def.add_unit_def(unit_cls_name="SteamCaboverRigidTruckGen2A")

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit",
        vehicle_length=4,
        cargo_length=4,
    )

    result.append(model_def)
    return result
