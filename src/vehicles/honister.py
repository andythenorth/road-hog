from road_vehicle import DumpHauler

consist = DumpHauler(id='honister',
                     base_numeric_id=230,
                     title='Honister [Dump Truck]',
                     vehicle_life=40,
                     intro_date=1947)

consist.add_unit(capacity=15,
                 vehicle_length=5,
                 effects=['EFFECT_SPRITE_DIESEL, -2, 1, 10'])

consist.add_unit(capacity=15,
                 vehicle_length=4)
