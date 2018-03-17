from road_vehicle import EdiblesTanker

consist = EdiblesTanker(id='beerwoods',
                        base_numeric_id=420,
                        title='Beerwoods [Edibles Tanker Truck]',
                        vehicle_life=40,
                        intro_date=1943)

consist.add_unit(capacity=15,
                 vehicle_length=5,
                 visual_effect='VISUAL_EFFECT_DIESEL')

consist.add_unit(capacity=15,
                 vehicle_length=4)

consist.add_model_variant(spritesheet_suffix=0)
