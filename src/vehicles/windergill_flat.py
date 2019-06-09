from road_vehicle import FlatbedTruckConsist, DieselVehicleUnit

consist = FlatbedTruckConsist(id='windergill_flat',
                       base_numeric_id=640,
                       name='Windergill',
                       gen=3)

consist.add_unit(type=DieselVehicleUnit,
                 vehicle_length=5,
                 cargo_length=3)

consist.add_unit(vehicle_length=4,
                 cargo_length=4)
