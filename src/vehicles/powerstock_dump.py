from road_vehicle import DumpHauler, DieselRoadVehicle

consist = DumpHauler(id='powerstock_dump',
                     base_numeric_id=340,
                     name='Powerstock',
                     semi_truck_so_redistribute_capacity=True,
                     vehicle_life=40,
                     gen=4,
                     intro_date=2001)

consist.add_unit(type=DieselRoadVehicle,
                 capacity=0,
                 vehicle_length=2,
                 semi_truck_shift_offset_jank=2,
                 effects=['EFFECT_SPRITE_DIESEL, -2, 1, 10',
                          'EFFECT_SPRITE_DIESEL, -2, -1, 10'],
                 always_use_same_spriterow=True)

consist.add_unit(capacity=40,
                 vehicle_length=7)
