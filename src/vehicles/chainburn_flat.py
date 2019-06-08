from road_vehicle import FlatbedTruckConsist, SteamVehicleUnit

consist = FlatbedTruckConsist(id='chainburn_flat',
                       base_numeric_id=630,
                       name='Chainburn',
                       vehicle_life=40,
                       gen=2)

consist.add_unit(type=SteamVehicleUnit,
                 capacity=12,
                 vehicle_length=5,
                 cargo_length=3,
                 effects=['EFFECT_SPRITE_STEAM, -3, 0, 12'])

consist.add_unit(capacity=12,
                 vehicle_length=4,
                 cargo_length=4)
