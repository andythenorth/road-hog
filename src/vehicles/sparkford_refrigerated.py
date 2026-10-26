from road_vehicle.model_def import ModelDef


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="RefrigeratedTram",
        model_id="sparkford_refrigerated",
        base_numeric_id=390,
        name="Sparkford",
        gen=3,
        intro_year_offset=10,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(
        unit_cls_name="ElectricVehicleUnit",
        vehicle_length=8,
        repeat=2,
    )

    result.append(model_def)
    return result
