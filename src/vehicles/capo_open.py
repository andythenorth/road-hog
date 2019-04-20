from road_vehicle import OpenHauler, DieselRoadVehicle

consist = OpenHauler(id='capo_open',
                     base_numeric_id=680,
                     name='Capo',
                     vehicle_life=40,
                     gen=4,
                     intro_date=1997)

consist.add_unit(type=DieselRoadVehicle,
                 capacity=20,
                 vehicle_length=5,
                 cargo_length=3,
                 effects=['EFFECT_SPRITE_DIESEL, -2, 1, 10'])

consist.add_unit(capacity=20,
                 vehicle_length=4,
                 cargo_length=3)
