from road_vehicle import BoxTramConsist, ElectricVehicleUnit

consist = BoxTramConsist(id='colbiggan_box',
                  base_numeric_id=880,
                  name='Colbiggan',
                  gen=3)

consist.add_unit(type=ElectricVehicleUnit,
                 vehicle_length=8,
                 repeat=2)
