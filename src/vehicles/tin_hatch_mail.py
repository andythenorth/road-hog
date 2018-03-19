from road_vehicle import MailHauler

consist = MailHauler(id='tin_hatch_mail',
                     base_numeric_id=820,
                     title='Tin Hatch [Courier Tram]',
                     tram_type='RAIL',
                     power=120,  # custom power
                     vehicle_life=40,
                     intro_date=1860)

consist.add_unit(capacity=0,
                 vehicle_length=3,
                 effect_spawn_model='EFFECT_SPAWN_MODEL_STEAM',
                 effects=['EFFECT_SPRITE_STEAM, -3, 0, 12', 'EFFECT_SPRITE_STEAM, 1, 0, 12'])

consist.add_unit(capacity=24,
                 vehicle_length=5)

