from road_vehicle import CoveredHopperTramConsist, ElectricVehicleUnit

consist = CoveredHopperTramConsist(id='polangrain_covered_hopper',
                            base_numeric_id=790,
                            name='Polangrain',
                              gen=2)

consist.add_unit(type=ElectricVehicleUnit,
                 vehicle_length=8,
                 repeat=2)
