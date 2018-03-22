from road_vehicle import OpenHauler

consist = OpenHauler(id='buildwas_open',
                     base_numeric_id=120,
                     name='Buildwas',
                     tram_type='RAIL',
                     vehicle_life=40,
                     intro_date=1860)

consist.add_unit(capacity=0,
                 vehicle_length=4,
                 effect_spawn_model='EFFECT_SPAWN_MODEL_STEAM',
                 effects=['EFFECT_SPRITE_STEAM, -2, 0, 14'],
                 always_use_same_spriterow=True)

consist.add_unit(capacity=16,
                 vehicle_length=4,
                 cargo_length=4,
                 repeat=3)
