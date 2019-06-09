from road_vehicle import CoveredHopperTruckConsist, DieselVehicleUnit

consist = CoveredHopperTruckConsist(id='limebreach_covered_hopper',
                             base_numeric_id=260,
                             name='Limebreach',
                             semi_truck_so_redistribute_capacity=True,
                                gen=3,
                             intro_date_offset=10)  # introduce later than gen epoch by design

consist.add_unit(type=DieselVehicleUnit,
                 vehicle_length=2,
                 semi_truck_shift_offset_jank=2,
                 effects=['EFFECT_SPRITE_DIESEL, -2, 1, 10'])

consist.add_unit(vehicle_length=5)
