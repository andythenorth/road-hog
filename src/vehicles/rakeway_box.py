from road_vehicle import BoxTram, ElectricRoadVehicle

consist = BoxTram(id='rakeway_box',
                  base_numeric_id=870,
                  name='Rakeway',
                  vehicle_life=40,
                  gen=2)

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=30,
                 vehicle_length=8,
                 repeat=2)
