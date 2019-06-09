from road_vehicle import LivestockTramConsist, SteamVehicleUnit

consist = LivestockTramConsist(id='scrag_end_livestock',
                        base_numeric_id=710,
                        name='Scrag End',
                             vehicle_life=40,
                        gen=1)

consist.add_unit(type=SteamVehicleUnit,
                 capacity=0,
                 vehicle_length=4,
                 effects=['EFFECT_SPRITE_STEAM, -2, 0, 14'],
                 always_use_same_spriterow=True)

consist.add_unit(vehicle_length=4,
                 repeat=3)
