from road_vehicle import OpenTruckConsist, DieselVehicleUnit

consist = OpenTruckConsist(id='yeoman_open',
                    base_numeric_id=170,
                    name='Yeoman',
                    semi_truck_so_redistribute_capacity=True,
                    vehicle_life=40,
                    gen=4)

consist.add_unit(type=DieselVehicleUnit,
                 vehicle_length=2,
                 semi_truck_shift_offset_jank=2,
                 always_use_same_spriterow=True)

consist.add_unit(vehicle_length=7,
                 cargo_length=7)
