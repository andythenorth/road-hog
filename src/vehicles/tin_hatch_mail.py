from road_vehicle import MailHauler, SteamRoadVehicle

consist = MailHauler(id='tin_hatch_mail',
                     base_numeric_id=820,
                     name='Tin Hatch',
                     tram_type='RAIL',
                     power=120,  # custom power
                     vehicle_life=40,
                     gen=4,                     intro_date=1860)

consist.add_unit(type=SteamRoadVehicle,
                 capacity=0,
                 vehicle_length=3,
                 effects=['EFFECT_SPRITE_STEAM, -3, 0, 12'],
                 always_use_same_spriterow=True)

consist.add_unit(capacity=24,
                 vehicle_length=5)
