from road_vehicle import SuppliesHauler
# equiv. Scammell Highwayman or Explorer with dolly low loader trailer - not huge

consist = SuppliesHauler(id='brigand_supplies',
                         base_numeric_id=540,
                         name='Brigand',
                         power=480,
                         vehicle_life=40,
                         intro_date=1953)

consist.add_unit(capacity=0,
                 vehicle_length=6,
                 visual_effect='VISUAL_EFFECT_DIESEL',
                 always_use_same_spriterow=True)

consist.add_unit(capacity=45,
                 vehicle_length=7)

consist.add_unit(capacity=0,
                 vehicle_length=6,
                 visual_effect='VISUAL_EFFECT_DIESEL',
                 unit_num_providing_spriterow_num=0,
                 always_use_same_spriterow=True)

