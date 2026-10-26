from road_vehicle.model_def import ModelDef

# 'inspired by' Scammell 100t low loader, but much smaller


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="SuppliesCake",
        model_id="crime_rigg_supplies",
        base_numeric_id=530,
        name="Crime Rigg",
        power=360,
        gen=2,
    )

    model_def.add_unit_def(
        unit_cls_name="SteamVehicleUnit",
        capacity=0,
        vehicle_length=5,
        effects=["EFFECT_SPRITE_STEAM, -3, 0, 12"],
        always_use_same_spriterow=True,
    )

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit",
        # capacity=45,
        vehicle_length=7,
    )

    model_def.add_unit_def(
        unit_cls_name="SteamVehicleUnit",
        capacity=0,
        vehicle_length=5,
        effects=["EFFECT_SPRITE_STEAM, -5, 0, 12"],
        # CABBAGE unit_num_providing_spriterow_num=0,
        always_use_same_spriterow=True,
    )

    result.append(model_def)
    return result
