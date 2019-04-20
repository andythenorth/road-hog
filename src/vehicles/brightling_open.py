from road_vehicle import OpenHauler, ElectricRoadVehicle

consist = OpenHauler(id='brightling_open',
                     base_numeric_id=90,
                     name='Brightling',
                     tram_type='ELRL',
                     vehicle_life=40,
                     gen=4,
                     intro_date=1940)

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=0,
                 vehicle_length=4,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 always_use_same_spriterow=True)

consist.add_unit(capacity=36,
                 vehicle_length=6,
                 cargo_length=3,
                 repeat=2)
