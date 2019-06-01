from road_vehicle import PaxLocalTramConsist, SteamRoadVehicle

consist = PaxLocalTramConsist(id='ladycross_pax',
                       base_numeric_id=0,
                       name='Ladycross',
                       vehicle_life=40,
                       gen=1)

consist.add_unit(type=SteamRoadVehicle,
                 capacity=0,
                 vehicle_length=4,
                 effects=['EFFECT_SPRITE_STEAM, -2, 0, 14'],
                 always_use_same_spriterow=True)

consist.add_unit(capacity=20,
                 vehicle_length=4,
                 repeat=3)
