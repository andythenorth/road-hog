from road_vehicle import DumpFeldbahn, ElectricRoadVehicle

consist = DumpFeldbahn(id='hake_lake_dump',
                       base_numeric_id=620,
                       name='Hake Lake',
                       vehicle_life=40,
                       gen=3)

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=0,
                 vehicle_length=4,
                 chassis='feldbahn_1',
                 always_use_same_spriterow=True)

consist.add_unit(capacity=28,
                 vehicle_length=4,
                 chassis='4_axle_feldbahn_16px',
                 repeat=7)
