from road_vehicle import LogHEQSConsist, SteamVehicleUnit

consist = LogHEQSConsist(id='trefell_log',
                  base_numeric_id=480,
                  name='Trefell',
                  power=100,  # custom power
                  gen=3)

consist.add_unit(base_platform=None, # no base platform by design currently
                 type=SteamVehicleUnit,
                 capacity=0,
                 vehicle_length=4,
                 effects=['EFFECT_SPRITE_STEAM, -5, 0, 12'],
                 always_use_same_spriterow=True)

consist.add_unit(base_platform=None, # no base platform by design currently
                 vehicle_length=6)
