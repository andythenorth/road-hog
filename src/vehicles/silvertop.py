from road_vehicle import EdiblesTanker

consist = EdiblesTanker(id='silvertop',
                        base_numeric_id=380,
                        title='Silvertop [Edibles Tanker Truck]',
                        vehicle_life=40,
                        intro_date=2001)

consist.add_unit(capacity=20,
                 vehicle_length=5,
                 effects=['EFFECT_SPRITE_DIESEL, -3, 1, 10'])

consist.add_unit(capacity=20,
                 vehicle_length=4)

consist.add_model_variant(spritesheet_suffix=0)
