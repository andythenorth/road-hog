from road_vehicle import LivestockTruckConsist, SteamVehicleUnit

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(
        schema_name="LivestockTruck",
        model_id="cowsleigh_livestock",
        base_numeric_id=900,
        name="Cowsleigh",
        gen=2,
        intro_year_offset=1,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(
        base_platform=None,  # only one instance of this one currently
        unit_cls_name="SteamVehicleUnit",
        vehicle_length=6,
        effects=["EFFECT_SPRITE_STEAM, -5, 0, 12"],
        always_use_same_spriterow=True,
    )  # !! because livestock gestalt only has one spriterow - could be done better??

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit", base_platform=None, vehicle_length=4
    )

    return [model_def]
