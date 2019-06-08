from road_vehicle import BoxTramConsist, ElectricVehicleUnit

consist = BoxTramConsist(id='rakeway_box',
                  base_numeric_id=870,
                  name='Rakeway',
                  vehicle_life=40,
                  gen=2)

consist.add_unit(type=ElectricVehicleUnit,
                 capacity=30,
                 vehicle_length=8,
                 repeat=2)
