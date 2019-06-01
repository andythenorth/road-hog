from road_vehicle import EdiblesTankerTramConsist, ElectricRoadVehicle

consist = EdiblesTankerTramConsist(id='poptop_edibles_tanker',
                            base_numeric_id=780,
                            name='Poptop',
                            vehicle_life=40,
                            gen=2,
                            intro_date_offset=6)  # introduce later than gen epoch by design

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=30,
                 vehicle_length=8,
                 repeat=2)
