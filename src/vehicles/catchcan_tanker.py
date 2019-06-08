from road_vehicle import TankerTramConsist, ElectricVehicleUnit

consist = TankerTramConsist(id='catchcan_tanker',
                     base_numeric_id=810,
                     name='Catchcan',
                     vehicle_life=40,
                     gen=2,
                     intro_date_offset=2)  # introduce later than gen epoch by design

consist.add_unit(type=ElectricVehicleUnit,
                 capacity=30,
                 vehicle_length=8,
                 repeat=2)
