from road_vehicle import OpenTruckConsist, SteamVehicleUnit

consist = OpenTruckConsist(id='jinglepot_open',
                    base_numeric_id=240,
                    name='Jinglepot',
                    gen=2)

consist.add_unit(type=SteamVehicleUnit,
                 vehicle_length=5,
                 cargo_length=3,
                 effects=['EFFECT_SPRITE_STEAM, -3, 0, 12'])

consist.add_unit(vehicle_length=4,
                 cargo_length=4)
