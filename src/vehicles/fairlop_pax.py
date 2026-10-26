from road_vehicle.model_def import ModelDef


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="PaxLocalTram",
        model_id="fairlop_pax",
        base_numeric_id=10,
        name="Fairlop",
        gen=2,
        intro_year_offset=3,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(
        unit_cls_name="ElectricVehicleUnit",
        vehicle_length=6,
        effects=["EFFECT_SPRITE_ELECTRIC, 0, 0, 12"],
    )

    model_def.add_unit_def(
        unit_cls_name="ElectricTrailerUnit",
        vehicle_length=5,
        repeat=2,
    )

    result.append(model_def)
    return result
