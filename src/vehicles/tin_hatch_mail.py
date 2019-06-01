from road_vehicle import MailTramConsist, SteamRoadVehicle

consist = MailTramConsist(id='tin_hatch_mail',
                   base_numeric_id=820,
                   name='Tin Hatch',
                   power=120,  # custom power
                   vehicle_life=40,
                   gen=1)

consist.add_unit(type=SteamRoadVehicle,
                 capacity=0,
                 vehicle_length=3,
                 effects=['EFFECT_SPRITE_STEAM, -3, 0, 12'],
                 always_use_same_spriterow=True)

consist.add_unit(capacity=24,
                 vehicle_length=5)
