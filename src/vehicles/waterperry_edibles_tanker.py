from road_vehicle import EdiblesTankerTruckConsist, DieselVehicleUnit

consist = EdiblesTankerTruckConsist(id='waterperry_edibles_tanker',
                             base_numeric_id=470,
                             name='Waterperry',
                             vehicle_life=40,
                             gen=4,
                             intro_date_offset=4)  # introduce later than gen epoch by design

consist.add_unit(type=DieselVehicleUnit,
                 capacity=20,
                 vehicle_length=5,
                 effects=['EFFECT_SPRITE_DIESEL, -2, 1, 10'])

consist.add_unit(capacity=20,
                 vehicle_length=4)
