from road_vehicle import OpenHauler

consist = OpenHauler(id='rattlebrook',
                     base_numeric_id=670,
                     title='Rattlebrook [Open Truck]',
                     vehicle_life=40,
                     intro_date=1939)

consist.add_unit(capacity=15,
                 vehicle_length=5,
                 cargo_length=3,
                 effects=['EFFECT_SPRITE_DIESEL, -2, 1, 10'])

consist.add_unit(capacity=15,
                 vehicle_length=4,
                 cargo_length=4,)
