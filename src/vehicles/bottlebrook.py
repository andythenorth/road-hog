from road_vehicle import EdiblesTanker

consist = EdiblesTanker(id='bottlebrook',
                        base_numeric_id=510,
                        title='Bottlebrook [Edibles Tanker Tram]',
                        tram_type='ELRL',
                        vehicle_life=40,
                        intro_date=1946)

consist.add_unit(capacity=36,
                 vehicle_length=8,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 repeat=2)

