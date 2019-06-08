from road_vehicle import FlatbedTramConsist, ElectricVehicleUnit

consist = FlatbedTramConsist(id='stancliffe_flat',
                      base_numeric_id=410,
                      name='Stancliffe',
                         vehicle_life=40,
                      gen=3)

consist.add_unit(type=ElectricVehicleUnit,
                 capacity=36,
                 vehicle_length=8,
                 cargo_length=3,
                 repeat=2)
