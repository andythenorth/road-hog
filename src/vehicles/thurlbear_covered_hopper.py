from road_vehicle import CoveredHopperTramConsist, ElectricRoadVehicle

consist = CoveredHopperTramConsist(id='thurlbear_covered_hopper',
                            base_numeric_id=460,
                            name='Thurlbear',
                            vehicle_life=40,
                            gen=3)

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=36,
                 vehicle_length=8,
                 repeat=2)
