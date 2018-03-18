from road_vehicle import EdiblesTanker

consist = EdiblesTanker(id='poptop',
                        base_numeric_id=780,
                        title='Poptop [Edibles Tanker Tram]',
                        tram_type='ELRL',
                        vehicle_life=40,
                        intro_date=1906)

consist.add_unit(capacity=30,
                 vehicle_length=8,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 repeat=2)

