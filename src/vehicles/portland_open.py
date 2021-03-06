from road_vehicle import OpenHauler, ElectricRoadVehicle

consist = OpenHauler(id='portland_open',
                     base_numeric_id=860,
                     name='Portland',
                     tram_type='ELRL',
                     vehicle_life=40,
                     intro_date=1900,)

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=30,
                 vehicle_length=8,
                 cargo_length=3,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 repeat=2)
