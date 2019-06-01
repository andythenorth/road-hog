from road_vehicle import CoveredHopperTramConsist, ElectricRoadVehicle

consist = CoveredHopperTramConsist(id='polangrain_covered_hopper',
                            base_numeric_id=790,
                            name='Polangrain',
                            vehicle_life=40,
                            gen=2)

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=30,
                 vehicle_length=8,
                 repeat=2)
