from road_vehicle import DumpFeldbahn, ElectricRoadVehicle

consist = DumpFeldbahn(id='hake_lake_dump',
                   base_numeric_id=620,
                   name='Hake Lake',
                   vehicle_life=40,
                   gen=4,
                   intro_date=1944)

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=0,
                 vehicle_length=4,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 always_use_same_spriterow=True)

consist.add_unit(capacity=36,
                 vehicle_length=6,
                 repeat=5)
