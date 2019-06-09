from road_vehicle import BoxTruckConsist, DieselVehicleUnit

consist = BoxTruckConsist(id='quickset_box',
                   base_numeric_id=350,
                   name='Quickset',
                   semi_truck_so_redistribute_capacity=True,
                   gen=4)

consist.add_unit(type=DieselVehicleUnit,
                 vehicle_length=2,
                 semi_truck_shift_offset_jank=2,
                 effects=['EFFECT_SPRITE_DIESEL, -2, 1, 10'])

consist.add_unit(vehicle_length=7)
