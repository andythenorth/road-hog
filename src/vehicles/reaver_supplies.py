from road_vehicle import SuppliesHauler, SteamRoadVehicle

consist = SuppliesHauler(id='reaver_supplies',
                         base_numeric_id=550,
                         name='Reaver',
                         power=240,  # custom power
                         vehicle_life=40,
                         gen=4,
                         intro_date=1875)

consist.add_unit(type=SteamRoadVehicle,
                 capacity=0,
                 vehicle_length=4,
                 effects=['EFFECT_SPRITE_STEAM, -5, 0, 12'],
                 always_use_same_spriterow=True)

consist.add_unit(capacity=45,
                 vehicle_length=7)

consist.add_unit(type=SteamRoadVehicle,
                 capacity=0,
                 vehicle_length=4,
                 effects=['EFFECT_SPRITE_STEAM, -5, 0, 12'],
                 unit_num_providing_spriterow_num=0,
                 always_use_same_spriterow=True)
