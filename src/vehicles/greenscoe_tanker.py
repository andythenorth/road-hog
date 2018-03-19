from road_vehicle import Tanker

consist = Tanker(id='greenscoe_tanker',
                 base_numeric_id=210,
                 title='Greenscoe [Tanker Truck]',
                 semi_truck_so_redistribute_capacity=True,
                 vehicle_life=40,
                 intro_date=1942)

consist.add_unit(capacity=0,
                 vehicle_length=2,
                 semi_truck_shift_offset_jank=2,
                 effects=['EFFECT_SPRITE_DIESEL, -3, 1, 10'],
                 always_use_same_spriterow=True)

consist.add_unit(capacity=30,
                 vehicle_length=5)
