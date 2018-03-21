from road_vehicle import Tanker

consist = Tanker(id='boilingwell_tanker',
                 base_numeric_id=920,
                 name='Boilingwell [Tanker Truck]',
                 semi_truck_so_redistribute_capacity=True,
                 vehicle_life=40,
                 intro_date=1915)

consist.add_unit(capacity=0,
                 vehicle_length=2,
                 semi_truck_shift_offset_jank=2,
                 effect_spawn_model='EFFECT_SPAWN_MODEL_STEAM',
                 effects=['EFFECT_SPRITE_STEAM, -3, 0, 12'],
                 always_use_same_spriterow=True)

consist.add_unit(capacity=24,
                 vehicle_length=5)
