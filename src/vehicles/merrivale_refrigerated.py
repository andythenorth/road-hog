from road_vehicle import RefrigeratedTruckConsist, DieselVehicleUnit

consist = RefrigeratedTruckConsist(id='merrivale_refrigerated',
                            base_numeric_id=300,
                            name='Merrivale',
                            semi_truck_so_redistribute_capacity=True,
                              gen=3,
                            intro_date_offset=10)  # introduce later than gen epoch by design

consist.add_unit(type=DieselVehicleUnit,
                 vehicle_length=2,
                 semi_truck_shift_offset_jank=2,
                 always_use_same_spriterow=True)

consist.add_unit(vehicle_length=6)
