from road_vehicle import OpenTruck, DieselRoadVehicle

consist = OpenTruck(id='capo_open',
                    base_numeric_id=680,
                    name='Capo',
                    vehicle_life=40,
                    gen=5)

consist.add_unit(type=DieselRoadVehicle,
                 capacity=20,
                 vehicle_length=5,
                 cargo_length=3,
                 effects=['EFFECT_SPRITE_DIESEL, -2, 1, 10'])

consist.add_unit(capacity=20,
                 vehicle_length=4,
                 cargo_length=3)
