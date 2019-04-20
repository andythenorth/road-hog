from road_vehicle import LivestockHauler, DieselRoadVehicle

consist = LivestockHauler(id='stungun_livestock',
                          base_numeric_id=430,
                          name='Stungun',
                          semi_truck_so_redistribute_capacity=True,
                          vehicle_life=40,
                          gen=4,
                          intro_date=1999)

consist.add_unit(type=DieselRoadVehicle,
                 capacity=0,
                 vehicle_length=2,
                 semi_truck_shift_offset_jank=2,
                 effects=['EFFECT_SPRITE_DIESEL, -2, 1, 10'])

consist.add_unit(capacity=40,
                 vehicle_length=8)
