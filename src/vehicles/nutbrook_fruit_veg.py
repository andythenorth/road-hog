from road_vehicle import FruitVegTramConsist, ElectricVehicleUnit

consist = FruitVegTramConsist(id='nutbrook_fruit_veg',
                       base_numeric_id=960,
                       name='Nutbrook',
                       gen=3)

consist.add_unit(type=ElectricVehicleUnit,
                 vehicle_length=8,
                 repeat=2)
