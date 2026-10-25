from road_vehicle import SuppliesCakeConsist, SteamVehicleUnit

from road_vehicle.model_def import ModelDef
# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.

# 'inspired by' Scammell 100t low loader, but much smaller


def main(roster_id):
    model_def = ModelDef(schema_name='SuppliesCake', 
        model_id="crime_rigg_supplies",
        base_numeric_id=530,
        name="Crime Rigg",
        power=360,
        gen=2,
    )

    model_def.add_unit_def(
        base_platform=None,  # no base platform by design currently
        unit_cls_name='SteamVehicleUnit',
        capacity=0,
        vehicle_length=5,
        effects=["EFFECT_SPRITE_STEAM, -3, 0, 12"],
        always_use_same_spriterow=True,
    )

    model_def.add_unit_def(unit_cls_name='RoadVehicleUnit', 
        base_platform=None,  # no base platform by design currently
        # capacity=45,
        vehicle_length=7,
    )

    model_def.add_unit_def(
        base_platform=None,  # no base platform by design currently
        unit_cls_name='SteamVehicleUnit',
        capacity=0,
        vehicle_length=5,
        effects=["EFFECT_SPRITE_STEAM, -5, 0, 12"],
        # CABBAGE unit_num_providing_spriterow_num=0,
        always_use_same_spriterow=True,
    )

    return [model_def]
