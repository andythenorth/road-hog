from road_vehicle import DumpHauler, ElectricRoadVehicle

consist = DumpHauler(id='hawkmoor_dump',
                     base_numeric_id=760,
                     name='Hawkmoor',
                     tram_type='ELRL',
                     vehicle_life=40,
                     intro_date=1902)

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=30,
                 vehicle_length=8,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 repeat=2)
