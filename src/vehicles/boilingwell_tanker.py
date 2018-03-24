from road_vehicle import Tanker, SteamRoadVehicle

consist = Tanker(id='boilingwell_tanker',
                 base_numeric_id=920,
                 name='Boilingwell',
                 semi_truck_so_redistribute_capacity=True,
                 vehicle_life=40,
                 intro_date=1915)

consist.add_unit(type=SteamRoadVehicle,
                 capacity=0,
                 vehicle_length=2,
                 semi_truck_shift_offset_jank=2,
                 effects=['EFFECT_SPRITE_STEAM, -3, 0, 12'],
                 always_use_same_spriterow=True)

consist.add_unit(capacity=24,
                 vehicle_length=5)
