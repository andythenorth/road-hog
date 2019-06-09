from road_vehicle import EdiblesTankerTramConsist, ElectricVehicleUnit

consist = EdiblesTankerTramConsist(id='bottlebrook_edibles_tanker',
                            base_numeric_id=510,
                            name='Bottlebrook',
                              gen=3,
                            intro_date_offset=6)  # introduce later than gen epoch by design

consist.add_unit(type=ElectricVehicleUnit,
                 vehicle_length=8,
                 repeat=2)
