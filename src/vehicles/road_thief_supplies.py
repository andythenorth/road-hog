from road_vehicle import SuppliesHauler

consist = SuppliesHauler(id='road_thief_supplies',
                         base_numeric_id=560,
                         name='Road Thief [Supplies Truck]',
                         power=720,
                         vehicle_life=40,
                         intro_date=1989)

consist.add_unit(capacity=0,
                 vehicle_length=7,
                 visual_effect='VISUAL_EFFECT_DIESEL',
                 always_use_same_spriterow=True)

consist.add_unit(capacity=45,
                 vehicle_length=7)

