from road_vehicle.model_def import ModelDef


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="CoveredHopperTruck",
        model_id="limebreach_covered_hopper",
        base_numeric_id=260,
        name="Limebreach",
        gen=3,
        intro_year_offset=10,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(
        unit_cls_name="DieselCaboverSemiTractorTruckGen3A",
    )

    model_def.add_unit_def(unit_cls_name="RoadVehicleUnit", vehicle_length=5)

    result.append(model_def)
    return result
