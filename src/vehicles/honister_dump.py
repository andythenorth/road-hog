from road_vehicle import DumpTruckConsist, DieselRoadVehicle

consist = DumpTruckConsist(id='honister_dump',
                    base_numeric_id=230,
                    name='Honister',
                    vehicle_life=40,
                    gen=3,
                    intro_date_offset=7)  # introduce later than gen epoch by design

consist.add_unit(type=DieselRoadVehicle,
                 capacity=15,
                 vehicle_length=5,
                 effects=['EFFECT_SPRITE_DIESEL, -2, 1, 10'])

consist.add_unit(capacity=15,
                 vehicle_length=4)
