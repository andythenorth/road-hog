from road_vehicle.model_def import ModelDef


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="OpenTruck",
        model_id="yeoman_open",
        base_numeric_id=170,
        name="Yeoman",
        gen=4,
    )

    model_def.add_unit_def(
        unit_cls_name="DieselConventionalCabSemiTractorTruckGen4A",
    )

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit",
        vehicle_length=7,
        cargo_length=7,
    )

    result.append(model_def)
    return result
