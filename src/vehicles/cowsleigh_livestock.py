from road_vehicle import LivestockTruckConsist, SteamVehicleUnit

from road_vehicle.model_def import ModelDef



def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="LivestockTruck",
        model_id="cowsleigh_livestock",
        base_numeric_id=900,
        name="Cowsleigh",
        gen=2,
        intro_year_offset=1,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(
        unit_cls_name="SteamVehicleUnit",
        vehicle_length=6,
        effects=["EFFECT_SPRITE_STEAM, -5, 0, 12"],
        always_use_same_spriterow=True,
    )  # !! because livestock gestalt only has one spriterow - could be done better??

    model_def.add_unit_def(unit_cls_name="RoadVehicleUnit", vehicle_length=4)

    result.append(model_def)
    return result
