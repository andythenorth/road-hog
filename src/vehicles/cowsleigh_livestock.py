from road_vehicle import LivestockHauler, SteamRoadVehicle

consist = LivestockHauler(id='cowsleigh_livestock',
                          base_numeric_id=900,
                          name='Cowsleigh',
                          vehicle_life=40,
                          gen=4,
                          intro_date=1911)

consist.add_unit(type=SteamRoadVehicle,
                 capacity=14,
                 vehicle_length=6,
                 effects=['EFFECT_SPRITE_STEAM, -5, 0, 12'])

consist.add_unit(capacity=10,
                 vehicle_length=4)
