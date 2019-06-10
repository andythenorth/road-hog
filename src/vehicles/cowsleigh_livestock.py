from road_vehicle import LivestockTruckConsist, SteamVehicleUnit

consist = LivestockTruckConsist(id='cowsleigh_livestock',
                         base_numeric_id=900,
                         name='Cowsleigh',
                           gen=2,
                         intro_date_offset=1)  # introduce later than gen epoch by design

consist.add_unit(base_platform=None, # only one instance of this one currently
                 type=SteamVehicleUnit,
                 vehicle_length=6,
                 effects=['EFFECT_SPRITE_STEAM, -5, 0, 12'])

consist.add_unit(base_platform=None,
                 vehicle_length=4)
