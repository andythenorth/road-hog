from road_vehicle import DumpTramConsist, ElectricVehicleUnit

consist = DumpTramConsist(id='nettlebridge_dump',
                   base_numeric_id=310,
                   name='Nettlebridge',
                   vehicle_life=40,
                   gen=3,
                   intro_date_offset=4)  # introduce later than gen epoch by design

consist.add_unit(type=ElectricVehicleUnit,
                 capacity=0,
                 vehicle_length=4,
                 always_use_same_spriterow=True)

consist.add_unit(vehicle_length=6,
                 repeat=2)
