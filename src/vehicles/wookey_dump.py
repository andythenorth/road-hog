from road_vehicle import DumpHauler, DieselRoadVehicle

consist = DumpHauler(id='wookey_dump',
                     base_numeric_id=490,
                     name='Wookey',
                     semi_truck_so_redistribute_capacity=True,
                     vehicle_life=40,
                     intro_date=1974)

consist.add_unit(type=DieselRoadVehicle,
                 capacity=0,
                 vehicle_length=2,
                 semi_truck_shift_offset_jank=2,
                 effects=['EFFECT_SPRITE_DIESEL, -2, 1, 10',
                          'EFFECT_SPRITE_DIESEL, -2, -1, 10'],
                 always_use_same_spriterow=True)

consist.add_unit(capacity=40,
                 vehicle_length=7)
