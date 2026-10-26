from road_vehicle import SuppliesCakeConsist, SteamVehicleUnit

from road_vehicle.model_def import ModelDef



def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="SuppliesCake",
        model_id="reaver_supplies",
        base_numeric_id=550,
        name="Reaver",
        power=240,  # custom power
        gen=1,
        intro_year_offset=15,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(
        unit_cls_name="SteamVehicleUnit",
        capacity=0,
        vehicle_length=4,
        effects=["EFFECT_SPRITE_STEAM, -5, 0, 12"],
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
        vehicle_length=4,
        effects=["EFFECT_SPRITE_STEAM, -5, 0, 12"],
        # CABBAGE unit_num_providing_spriterow_num=0,
        always_use_same_spriterow=True,
    )

    result.append(model_def)
    return result
