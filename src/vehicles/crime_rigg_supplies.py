from road_vehicle import SuppliesHauler, SteamRoadVehicle
# 'inspired by' Scammell 100t low loader, but much smaller

consist = SuppliesHauler(id='crime_rigg_supplies',
                         base_numeric_id=530,
                         name='Crime Rigg',
                         power=360,
                         vehicle_life=40,
                         gen=4,
                         intro_date=1920)

consist.add_unit(type=SteamRoadVehicle,
                 capacity=0,
                 vehicle_length=5,
                 effects=['EFFECT_SPRITE_STEAM, -3, 0, 12'],
                 always_use_same_spriterow=True)

consist.add_unit(capacity=45,
                 vehicle_length=7)

consist.add_unit(type=SteamRoadVehicle,
                 capacity=0,
                 vehicle_length=5,
                 effects=['EFFECT_SPRITE_STEAM, -5, 0, 12'],
                 unit_num_providing_spriterow_num=0,
                 always_use_same_spriterow=True)
