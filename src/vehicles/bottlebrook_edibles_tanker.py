from road_vehicle import EdiblesTanker, ElectricRoadVehicle

consist = EdiblesTanker(id='bottlebrook_edibles_tanker',
                        base_numeric_id=510,
                        name='Bottlebrook',
                        tram_type='ELRL',
                        vehicle_life=40,
                        gen=4,
                        intro_date=1946)

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=36,
                 vehicle_length=8,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 repeat=2)
