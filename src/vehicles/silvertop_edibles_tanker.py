from road_vehicle import EdiblesTankerTruckConsist, DieselVehicleUnit

consist = EdiblesTankerTruckConsist(id='silvertop_edibles_tanker',
                             base_numeric_id=380,
                             name='Silvertop',
                             vehicle_life=40,
                             gen=5,
                             intro_date_offset=4)  # introduce later than gen epoch by design

consist.add_unit(type=DieselVehicleUnit,
                 vehicle_length=5,
                 effects=['EFFECT_SPRITE_DIESEL, -3, 1, 10'])

consist.add_unit(vehicle_length=4)
