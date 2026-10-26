from road_vehicle.model_def import ModelDef


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="TankerTruck",
        model_id="meriden_tanker",
        base_numeric_id=290,
        name="Meriden",
        gen=4,
        intro_year_offset=6,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(
        unit_cls_name="DieselCaboverSemiTractorTruckGen4A",
    )

    model_def.add_unit_def(unit_cls_name="RoadVehicleUnit", vehicle_length=7)

    result.append(model_def)
    return result
