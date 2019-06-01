from road_vehicle import LivestockTruckConsist, SteamRoadVehicle

consist = LivestockTruckConsist(id='cowsleigh_livestock',
                         base_numeric_id=900,
                         name='Cowsleigh',
                         vehicle_life=40,
                         gen=2,
                         intro_date_offset=1)  # introduce later than gen epoch by design

consist.add_unit(type=SteamRoadVehicle,
                 capacity=14,
                 vehicle_length=6,
                 effects=['EFFECT_SPRITE_STEAM, -5, 0, 12'])

consist.add_unit(capacity=10,
                 vehicle_length=4)
