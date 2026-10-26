from road_vehicle.model_def import ModelDef


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="LogHEQS",
        model_id="griff_log",
        base_numeric_id=220,
        name="Griff",
        power=100,  # custom power
        gen=1,
        intro_year_offset=10,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(
        unit_cls_name="SteamVehicleUnit",
        capacity=0,
        vehicle_length=4,
        effects=["EFFECT_SPRITE_AIRCRAFT_BREAKDOWN_SMOKE, -5, 0, 12"],
        always_use_same_spriterow=True,
    )

    model_def.add_unit_def(unit_cls_name="RoadVehicleUnit", vehicle_length=6)

    result.append(model_def)
    return result
