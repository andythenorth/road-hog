from road_vehicle import TankerTramConsist, ElectricVehicleUnit

consist = TankerTramConsist(id='oylbarral_tanker',
                     base_numeric_id=320,
                     name='Oylbarral',
                      gen=3,
                     intro_date_offset=4)  # introduce later than gen epoch by design

consist.add_unit(base_platform=None, # no base platform by design currently
                 type=ElectricVehicleUnit,
                 capacity=0,
                 vehicle_length=4,
                 always_use_same_spriterow=True)

consist.add_unit(base_platform=None, # no base platform by design currently
                 vehicle_length=6,
                 repeat=2)
