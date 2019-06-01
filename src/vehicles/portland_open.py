from road_vehicle import OpenTramConsist, ElectricRoadVehicle

consist = OpenTramConsist(id='portland_open',
                   base_numeric_id=860,
                   name='Portland',
                   vehicle_life=40,
                   gen=2)

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=30,
                 vehicle_length=8,
                 cargo_length=3,
                 repeat=2)
