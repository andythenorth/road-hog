from road_vehicle import EdiblesTankerTruckConsist, SteamRoadVehicle

consist = EdiblesTankerTruckConsist(id='flow_edge_edibles_tanker',
                             base_numeric_id=930,
                             name='Flow Edge',
                             vehicle_life=40,
                             gen=2,
                             intro_date_offset=2)  # introduce later than gen epoch by design

consist.add_unit(type=SteamRoadVehicle,
                 capacity=12,
                 vehicle_length=5)

consist.add_unit(capacity=12,
                 vehicle_length=4)
