from road_vehicle import LogHauler, SteamRoadVehicle

consist = LogHauler(id='trefell_log',
                    base_numeric_id=480,
                    name='Trefell',
                    road_type='HAUL',
                    power=100,  # custom power
                    vehicle_life=40,
                    gen=4,
                    intro_date=1910)

consist.add_unit(type=SteamRoadVehicle,
                 capacity=0,
                 vehicle_length=4,
                 effects=['EFFECT_SPRITE_STEAM, -5, 0, 12'],
                 always_use_same_spriterow=True)

consist.add_unit(capacity=40,
                 vehicle_length=6)
