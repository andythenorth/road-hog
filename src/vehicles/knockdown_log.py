from road_vehicle import LogHEQS, DieselRoadVehicle

consist = LogHEQS(id='knockdown_log',
                   base_numeric_id=250,
                   name='Knockdown',
                   power=250,  # custom power
                   speed=50,
                   vehicle_life=40,
                   gen=3)

consist.add_unit(type=DieselRoadVehicle,
                 capacity=30,
                 vehicle_length=7)

consist.add_unit(capacity=30,
                 vehicle_length=6)
