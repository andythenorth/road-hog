from road_vehicle import DumpHauler, DieselRoadVehicle

consist = DumpHauler(id='honister_dump',
                     base_numeric_id=230,
                     name='Honister',
                     vehicle_life=40,
                     intro_date=1947)

consist.add_unit(type=DieselRoadVehicle,
                 capacity=15,
                 vehicle_length=5,
                 effects=['EFFECT_SPRITE_DIESEL, -2, 1, 10'])

consist.add_unit(capacity=15,
                 vehicle_length=4)
