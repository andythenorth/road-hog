from road_vehicle import RefrigeratedHauler, DieselRoadVehicle

consist = RefrigeratedHauler(id='merrivale_refrigerated',
                             base_numeric_id=300,
                             name='Merrivale',
                             semi_truck_so_redistribute_capacity=True,
                             vehicle_life=40,
                             gen=3,
                             intro_date_offset=10)  # introduce later than gen epoch by design

consist.add_unit(type=DieselRoadVehicle,
                 capacity=0,
                 vehicle_length=2,
                 semi_truck_shift_offset_jank=2,
                 always_use_same_spriterow=True)

consist.add_unit(capacity=30,
                 vehicle_length=6)
