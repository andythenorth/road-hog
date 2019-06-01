from road_vehicle import FruitVegTramConsist, SteamRoadVehicle

consist = FruitVegTramConsist(id='plumley_fruit_veg',
                       base_numeric_id=950,
                       name='Plumley',
                       vehicle_life=40,
                       gen=1,
                       intro_date_offset=1)  # introduce later than gen epoch by design

consist.add_unit(type=SteamRoadVehicle,
                 capacity=0,
                 vehicle_length=4,
                 effects=['EFFECT_SPRITE_STEAM, -2, 0, 14'],
                 always_use_same_spriterow=True)

consist.add_unit(capacity=16,
                 vehicle_length=4,
                 repeat=3)
