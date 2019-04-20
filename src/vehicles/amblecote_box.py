from road_vehicle import BoxHauler, SteamRoadVehicle

consist = BoxHauler(id='amblecote_box',
                    base_numeric_id=80,
                    name='Amblecote',
                    tram_type='RAIL',
                    vehicle_life=40,
                    gen=4,                    intro_date=1860)

consist.add_unit(type=SteamRoadVehicle,
                 capacity=0,
                 vehicle_length=4,
                 effects=['EFFECT_SPRITE_STEAM, -2, 0, 14'],
                 always_use_same_spriterow=True)

consist.add_unit(capacity=16,
                 vehicle_length=4,
                 repeat=3)
