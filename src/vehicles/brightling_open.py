from road_vehicle import OpenTram, ElectricRoadVehicle

consist = OpenTram(id='brightling_open',
                   base_numeric_id=90,
                   name='Brightling',
                   vehicle_life=40,
                   gen=3)

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=0,
                 vehicle_length=4,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 always_use_same_spriterow=True)

consist.add_unit(capacity=36,
                 vehicle_length=6,
                 cargo_length=3,
                 repeat=2)
