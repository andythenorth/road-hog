from road_vehicle import LogHauler, SteamRoadVehicle

consist = LogHauler(id='griff_log',
                    base_numeric_id=220,
                    name='Griff',
                    road_type='HAUL',
                    power=100,  # custom power
                    vehicle_life=40,
                    intro_date=1870)

consist.add_unit(type=SteamRoadVehicle,
                 capacity=0,
                 vehicle_length=4,
                 effects=['EFFECT_SPRITE_AIRCRAFT_BREAKDOWN_SMOKE, -5, 0, 12'],
                 always_use_same_spriterow=True)

consist.add_unit(capacity=40,
                 vehicle_length=6)
