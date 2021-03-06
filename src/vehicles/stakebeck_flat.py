from road_vehicle import FlatHauler, SteamRoadVehicle

consist = FlatHauler(id='stakebeck_flat',
                        base_numeric_id=750,
                        name='Stakebeck',
                        tram_type='RAIL',
                        vehicle_life=40,
                        intro_date=1860)

consist.add_unit(type=SteamRoadVehicle,
                 capacity=0,
                 vehicle_length=4,
                 effects=['EFFECT_SPRITE_STEAM, -2, 0, 14'],
                 always_use_same_spriterow=True)

consist.add_unit(capacity=16,
                 vehicle_length=4,
                 cargo_length=4,
                 repeat=3)
