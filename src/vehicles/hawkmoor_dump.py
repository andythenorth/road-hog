from road_vehicle import DumpTramConsist, ElectricRoadVehicle

consist = DumpTramConsist(id='hawkmoor_dump',
                   base_numeric_id=760,
                   name='Hawkmoor',
                   vehicle_life=40,
                   gen=2,
                   intro_date_offset=2)  # introduce later than gen epoch by design

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=30,
                 vehicle_length=8,
                 repeat=2)
