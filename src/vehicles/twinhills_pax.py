from road_vehicle import PaxLocalTram, ElectricRoadVehicle

consist = PaxLocalTram(id='twinhills_pax',
                       base_numeric_id=70,
                       name='Twinhills',
                       vehicle_life=40,
                       gen=5)

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=70,
                 vehicle_length=8,
                 repeat=2)
