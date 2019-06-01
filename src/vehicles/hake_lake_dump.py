from road_vehicle import DumpFeldbahnConsist, ElectricRoadVehicle

consist = DumpFeldbahnConsist(id='hake_lake_dump',
                       base_numeric_id=620,
                       name='Hake Lake',
                       vehicle_life=40,
                       gen=3)

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=0,
                 chassis='feldbahn_1_16px',
                 always_use_same_spriterow=True)

consist.add_unit(capacity=28,
                 chassis='4_axle_feldbahn_16px',
                 repeat=7)
