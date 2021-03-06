from road_vehicle import DumpHauler

consist = DumpHauler(id='gravelhead_dump',
                     base_numeric_id=580,
                     name='Gravelhead',
                     power=130,
                     vehicle_life=40,
                     intro_date=1920)

consist.add_unit(capacity=12,
                 vehicle_length=6,
                 effect_spawn_model='EFFECT_SPAWN_MODEL_STEAM',
                 effects=['EFFECT_SPRITE_STEAM, -3, 0, 12'])

consist.add_unit(capacity=12,
                 vehicle_length=5)
