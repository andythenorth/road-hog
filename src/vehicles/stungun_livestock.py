from road_vehicle import LivestockTruckConsist, DieselVehicleUnit

consist = LivestockTruckConsist(id='stungun_livestock',
                         base_numeric_id=430,
                         name='Stungun',
                         semi_truck_so_redistribute_capacity=True,
                         vehicle_life=40,
                         gen=5,
                         intro_date_offset=2)  # introduce later than gen epoch by design

consist.add_unit(type=DieselVehicleUnit,
                 vehicle_length=2,
                 semi_truck_shift_offset_jank=2,
                 effects=['EFFECT_SPRITE_DIESEL, -2, 1, 10'])

consist.add_unit(vehicle_length=8)
