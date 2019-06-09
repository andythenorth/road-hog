from road_vehicle import BoxTramConsist, SteamVehicleUnit

consist = BoxTramConsist(id='amblecote_box',
                  base_numeric_id=80,
                  name='Amblecote',
                  gen=1)

consist.add_unit(type=SteamVehicleUnit,
                 capacity=0,
                 vehicle_length=4,
                 effects=['EFFECT_SPRITE_STEAM, -2, 0, 14'],
                 always_use_same_spriterow=True)

consist.add_unit(vehicle_length=4,
                 repeat=3)
