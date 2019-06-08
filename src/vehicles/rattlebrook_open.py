from road_vehicle import OpenTruckConsist, DieselVehicleUnit

consist = OpenTruckConsist(id='rattlebrook_open',
                    base_numeric_id=670,
                    name='Rattlebrook',
                    vehicle_life=40,
                    gen=3)

consist.add_unit(type=DieselVehicleUnit,
                 capacity=15,
                 vehicle_length=5,
                 cargo_length=3,
                 effects=['EFFECT_SPRITE_DIESEL, -2, 1, 10'])

consist.add_unit(capacity=15,
                 vehicle_length=4,
                 cargo_length=4,)
