from road_vehicle import LogHEQSConsist, DieselVehicleUnit

consist = LogHEQSConsist(id='buff_log',
                  base_numeric_id=110,
                  name='Buff',
                  power=550,
                  speed=60,
                  vehicle_life=40,
                  gen=4)

consist.add_unit(type=DieselVehicleUnit,
                 #capacity=40,
                 vehicle_length=7)

consist.add_unit(#capacity=35,
                 vehicle_length=8)
