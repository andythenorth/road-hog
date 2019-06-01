from road_vehicle import FruitVegTramConsist, ElectricRoadVehicle

consist = FruitVegTramConsist(id='nutbrook_fruit_veg',
                       base_numeric_id=960,
                       name='Nutbrook',
                       vehicle_life=40,
                       gen=3)

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=36,
                 vehicle_length=8,
                 repeat=2)
