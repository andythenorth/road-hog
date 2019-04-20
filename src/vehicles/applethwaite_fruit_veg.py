from road_vehicle import FruitVegHauler, ElectricRoadVehicle

consist = FruitVegHauler(id='applethwaite_fruit_veg',
                         base_numeric_id=940,
                         name='Applethwaite',
                         tram_type='ELRL',
                         vehicle_life=40,
                         gen=4,
                         intro_date=1901)

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=30,
                 vehicle_length=8,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 repeat=2)
