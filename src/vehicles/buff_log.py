from road_vehicle import LogHEQSConsist, DieselVehicleUnit

consist = LogHEQSConsist(id='buff_log',
                  base_numeric_id=110,
                  name='Buff',
                  power=550,
                  speed=60,
                  gen=4)

consist.add_unit(base_platform=None, # no base platform by design currently
                 type=DieselVehicleUnit,
                 #capacity=40,
                 vehicle_length=7)

consist.add_unit(base_platform=None, # no base platform by design currently
                 #capacity=35,
                 vehicle_length=8)
