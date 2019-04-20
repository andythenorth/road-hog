from road_vehicle import DumpHauler, SteamRoadVehicle

consist = DumpHauler(id='coleman_dump',
                     base_numeric_id=910,
                     name='Coleman',
                     semi_truck_so_redistribute_capacity=True,
                     vehicle_life=40,
                     gen=2,
                     intro_date_offset=7)  # introduce later than gen epoch by design

consist.add_unit(type=SteamRoadVehicle,
                 capacity=0,
                 vehicle_length=2,
                 semi_truck_shift_offset_jank=2,
                 effects=['EFFECT_SPRITE_STEAM, -3, 0, 12'],
                 always_use_same_spriterow=True)

consist.add_unit(capacity=24,
                 vehicle_length=5)
