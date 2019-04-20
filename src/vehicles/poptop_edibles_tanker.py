from road_vehicle import EdiblesTankerTram, ElectricRoadVehicle

consist = EdiblesTankerTram(id='poptop_edibles_tanker',
                            base_numeric_id=780,
                            name='Poptop',
                            tram_type='ELRL',
                            vehicle_life=40,
                            gen=2,
                            intro_date_offset=6)  # introduce later than gen epoch by design

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=30,
                 vehicle_length=8,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 repeat=2)
