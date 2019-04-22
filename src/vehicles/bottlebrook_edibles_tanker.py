from road_vehicle import EdiblesTankerTram, ElectricRoadVehicle

consist = EdiblesTankerTram(id='bottlebrook_edibles_tanker',
                            base_numeric_id=510,
                            name='Bottlebrook',
                            vehicle_life=40,
                            gen=3,
                            intro_date_offset=6)  # introduce later than gen epoch by design

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=36,
                 vehicle_length=8,
                 repeat=2)
