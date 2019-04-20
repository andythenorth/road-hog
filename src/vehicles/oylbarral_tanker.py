from road_vehicle import Tanker, ElectricRoadVehicle

consist = Tanker(id='oylbarral_tanker',
                 base_numeric_id=320,
                 name='Oylbarral',
                 tram_type='ELRL',
                 vehicle_life=40,
                 gen=4,                 intro_date=1945)

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=0,
                 vehicle_length=4,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 always_use_same_spriterow=True)

consist.add_unit(capacity=36,
                 vehicle_length=6,
                 repeat=2)
