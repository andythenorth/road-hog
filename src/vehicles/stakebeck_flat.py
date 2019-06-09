from road_vehicle import FlatbedTramConsist, SteamVehicleUnit

consist = FlatbedTramConsist(id='stakebeck_flat',
                      base_numeric_id=750,
                      name='Stakebeck',
                        gen=1)

consist.add_unit(type=SteamVehicleUnit,
                 capacity=0,
                 vehicle_length=4,
                 effects=['EFFECT_SPRITE_STEAM, -2, 0, 14'],
                 always_use_same_spriterow=True)

consist.add_unit(vehicle_length=4,
                 cargo_length=4,
                 repeat=3)
