from road_vehicle.model_def import ModelDef


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="RefrigeratedTruck",
        model_id="merrivale_refrigerated",
        base_numeric_id=300,
        name="Merrivale",
        gen=3,
        intro_year_offset=10,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(
        unit_cls_name="DieselConventionalCabSemiTractorTruckGen3A",
    )

    model_def.add_unit_def(unit_cls_name="RoadVehicleUnit", vehicle_length=6)

    result.append(model_def)
    return result
