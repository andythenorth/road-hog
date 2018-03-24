from road_vehicle import CoveredHopperHauler, DieselRoadVehicle

consist = CoveredHopperHauler(id='limebreach_covered_hopper',
                              base_numeric_id=260,
                              name='Limebreach',
                              semi_truck_so_redistribute_capacity=True,
                              vehicle_life=40,
                              intro_date=1949)

consist.add_unit(type=DieselRoadVehicle,
                 capacity=0,
                 vehicle_length=2,
                 semi_truck_shift_offset_jank=2,
                 effects=['EFFECT_SPRITE_DIESEL, -2, 1, 10'])

consist.add_unit(capacity=30,
                 vehicle_length=5)
