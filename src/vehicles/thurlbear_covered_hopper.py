from road_vehicle import CoveredHopperTramConsist, ElectricVehicleUnit

consist = CoveredHopperTramConsist(id='thurlbear_covered_hopper',
                            base_numeric_id=460,
                            name='Thurlbear',
                            vehicle_life=40,
                            gen=3)

consist.add_unit(type=ElectricVehicleUnit,
                 capacity=36,
                 vehicle_length=8,
                 repeat=2)
