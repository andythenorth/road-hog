from road_vehicle import EdiblesTanker, DieselRoadVehicle

consist = EdiblesTanker(id='silvertop_edibles_tanker',
                        base_numeric_id=380,
                        name='Silvertop',
                        vehicle_life=40,
                        gen=4,
                        intro_date=2001)

consist.add_unit(type=DieselRoadVehicle,
                 capacity=20,
                 vehicle_length=5,
                 effects=['EFFECT_SPRITE_DIESEL, -3, 1, 10'])

consist.add_unit(capacity=20,
                 vehicle_length=4)
