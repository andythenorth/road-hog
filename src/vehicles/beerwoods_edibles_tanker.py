from road_vehicle import EdiblesTankerTruckConsist, DieselVehicleUnit

consist = EdiblesTankerTruckConsist(id='beerwoods_edibles_tanker',
                             base_numeric_id=420,
                             name='Beerwoods',
                             vehicle_life=40,
                             gen=3,
                             intro_date_offset=4)  # introduce later than gen epoch by design

consist.add_unit(type=DieselVehicleUnit,
                 vehicle_length=5)

consist.add_unit(vehicle_length=4)
