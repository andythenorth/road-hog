from road_vehicle import DumpTruckConsist, DieselVehicleUnit

consist = DumpTruckConsist(id='honister_dump',
                    base_numeric_id=230,
                    name='Honister',
                    gen=3,
                    intro_date_offset=7)  # introduce later than gen epoch by design

consist.add_unit(type=DieselVehicleUnit,
                 vehicle_length=5,
                 effects=['EFFECT_SPRITE_DIESEL, -2, 1, 10'])

consist.add_unit(base_platform=None,
                 vehicle_length=4)
