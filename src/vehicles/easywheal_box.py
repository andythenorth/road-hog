from road_vehicle import BoxTruckConsist, DieselVehicleUnit

consist = BoxTruckConsist(id='easywheal_box',
                   base_numeric_id=160,
                   name='Easywheal',
                   semi_truck_so_redistribute_capacity=True,
                   vehicle_life=40,
                   gen=3)

consist.add_unit(type=DieselVehicleUnit,
                 capacity=0,
                 vehicle_length=2,
                 semi_truck_shift_offset_jank=2,
                 always_use_same_spriterow=True)

consist.add_unit(capacity=30,
                 vehicle_length=5)
