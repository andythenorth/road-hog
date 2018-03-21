from road_vehicle import EdiblesTanker

consist = EdiblesTanker(id='waterperry_edibles_tanker',
                        base_numeric_id=470,
                        name='Waterperry [Edibles Tanker Truck]',
                        vehicle_life=40,
                        intro_date=1972)

consist.add_unit(capacity=20,
                 vehicle_length=5,
                 effects=['EFFECT_SPRITE_DIESEL, -2, 1, 10'])

consist.add_unit(capacity=20,
                 vehicle_length=4)

