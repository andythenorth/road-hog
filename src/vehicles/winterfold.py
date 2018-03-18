from road_vehicle import RefrigeratedHauler

consist = RefrigeratedHauler(id='winterfold',
                             base_numeric_id=770,
                             title='Winterfold [Reefer Tram]',
                             tram_type='ELRL',
                             vehicle_life=40,
                             intro_date=1915)

consist.add_unit(capacity=30,
                 vehicle_length=8,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 repeat=2)

