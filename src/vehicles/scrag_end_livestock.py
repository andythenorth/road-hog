from road_vehicle import LivestockTram, SteamRoadVehicle

consist = LivestockTram(id='scrag_end_livestock',
                        base_numeric_id=710,
                        name='Scrag End',
                        tram_type='RAIL',
                        vehicle_life=40,
                        gen=1)

consist.add_unit(type=SteamRoadVehicle,
                 capacity=0,
                 vehicle_length=4,
                 effects=['EFFECT_SPRITE_STEAM, -2, 0, 14'],
                 always_use_same_spriterow=True)

consist.add_unit(capacity=16,
                 vehicle_length=4,
                 repeat=3)
