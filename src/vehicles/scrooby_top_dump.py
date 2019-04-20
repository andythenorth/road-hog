from road_vehicle import DumpHauler, SteamRoadVehicle

consist = DumpHauler(id='scrooby_top_dump',
                     base_numeric_id=700,
                     name='Scrooby Top',
                     tram_type='RAIL',
                     vehicle_life=40,
                     gen=1,
                     intro_date_offset=10)  # introduce later than gen epoch by design

consist.add_unit(type=SteamRoadVehicle,
                 capacity=0,
                 vehicle_length=4,
                 effects=['EFFECT_SPRITE_STEAM, -3, 0, 12'],
                 always_use_same_spriterow=True)

consist.add_unit(capacity=12,
                 vehicle_length=3,
                 repeat=4)
