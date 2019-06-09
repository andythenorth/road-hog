from road_vehicle import FlatbedTramConsist, ElectricVehicleUnit

consist = FlatbedTramConsist(id='stancliffe_flat',
                      base_numeric_id=410,
                      name='Stancliffe',
                        gen=3)

consist.add_unit(type=ElectricVehicleUnit,
                 vehicle_length=8,
                 cargo_length=3,
                 repeat=2)
