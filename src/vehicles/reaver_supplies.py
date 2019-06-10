from road_vehicle import SuppliesCakeConsist, SteamVehicleUnit

consist = SuppliesCakeConsist(id='reaver_supplies',
                       base_numeric_id=550,
                       name='Reaver',
                       power=240,  # custom power
                       gen=1,
                       intro_date_offset=15)  # introduce later than gen epoch by design

consist.add_unit(base_platform=None, # no base platform by design currently
                 type=SteamVehicleUnit,
                 capacity=0,
                 vehicle_length=4,
                 effects=['EFFECT_SPRITE_STEAM, -5, 0, 12'],
                 always_use_same_spriterow=True)

consist.add_unit(base_platform=None, # no base platform by design currently
                 #capacity=45,
                 vehicle_length=7)

consist.add_unit(base_platform=None, # no base platform by design currently
                 type=SteamVehicleUnit,
                 capacity=0,
                 vehicle_length=4,
                 effects=['EFFECT_SPRITE_STEAM, -5, 0, 12'],
                 unit_num_providing_spriterow_num=0,
                 always_use_same_spriterow=True)
