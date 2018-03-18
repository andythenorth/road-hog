from road_vehicle import FruitVegHauler

consist = FruitVegHauler(id='applethwaite',
                         base_numeric_id=940,
                         title='Applethwaite [Fruit Tram]',
                         tram_type='ELRL',
                         vehicle_life=40,
                         intro_date=1901)

consist.add_unit(capacity=30,
                 vehicle_length=8,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 repeat=2)

