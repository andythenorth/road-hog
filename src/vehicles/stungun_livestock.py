from road_vehicle.model_def import ModelDef


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="LivestockTruck",
        model_id="stungun_livestock",
        base_numeric_id=430,
        name="Stungun",
        gen=5,
        intro_year_offset=2,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(
        unit_cls_name="DieselCaboverSemiTractorTruckGen5A",
    )

    model_def.add_unit_def(unit_cls_name="RoadVehicleUnit", vehicle_length=8)

    result.append(model_def)
    return result
