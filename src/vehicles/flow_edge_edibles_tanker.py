from road_vehicle import EdiblesTankerTruckConsist, SteamVehicleUnit

consist = EdiblesTankerTruckConsist(id='flow_edge_edibles_tanker',
                             base_numeric_id=930,
                             name='Flow Edge',
                                gen=2,
                             intro_date_offset=2)  # introduce later than gen epoch by design

consist.add_unit(type=SteamVehicleUnit,
                 vehicle_length=5)

consist.add_unit(vehicle_length=4)
