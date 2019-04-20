from road_vehicle import TankerTram, ElectricRoadVehicle

consist = TankerTram(id='oylbarral_tanker',
                     base_numeric_id=320,
                     name='Oylbarral',
                     tram_type='ELRL',
                     vehicle_life=40,
                     gen=3,
                     intro_date_offset=4)  # introduce later than gen epoch by design

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=0,
                 vehicle_length=4,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 always_use_same_spriterow=True)

consist.add_unit(capacity=36,
                 vehicle_length=6,
                 repeat=2)
