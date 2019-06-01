from road_vehicle import BoxTramConsist, ElectricRoadVehicle

consist = BoxTramConsist(id='colbiggan_box',
                  base_numeric_id=880,
                  name='Colbiggan',
                  vehicle_life=40,
                  gen=3)

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=36,
                 vehicle_length=8,
                 repeat=2)
