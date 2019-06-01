from road_vehicle import LivestockTramConsist, ElectricRoadVehicle

consist = LivestockTramConsist(id='trotalong_livestock',
                        base_numeric_id=720,
                        name='Trotalong',
                        vehicle_life=40,
                        gen=2,
                        intro_date_offset=1)  # introduce later than gen epoch by design

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=30,
                 vehicle_length=8,
                 repeat=2)
