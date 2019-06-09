from road_vehicle import FlatbedTramConsist, ElectricVehicleUnit

consist = FlatbedTramConsist(id='rackwood_flat',
                      base_numeric_id=740,
                      name='Rackwood',
                        gen=2)

consist.add_unit(type=ElectricVehicleUnit,
                 vehicle_length=8,
                 cargo_length=3,
                 repeat=2)
