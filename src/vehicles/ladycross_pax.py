from road_vehicle import PaxLocalTramConsist, SteamVehicleUnit

consist = PaxLocalTramConsist(id='ladycross_pax',
                       base_numeric_id=0,
                       name='Ladycross',
                       gen=1)

consist.add_unit(base_platform=None, # pax trams have no base platform by design currently
                 type=SteamVehicleUnit,
                 capacity=0,
                 vehicle_length=4,
                 effects=['EFFECT_SPRITE_STEAM, -2, 0, 14'],
                 always_use_same_spriterow=True)

consist.add_unit(base_platform=None, # pax trams have no base platform by design currently
                 vehicle_length=4,
                 repeat=3)
