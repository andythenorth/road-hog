from road_vehicle import MailHauler, DieselRoadVehicle

consist = MailHauler(id='brass_monkey_mail',
                     base_numeric_id=570,
                     name='Brass Monkey',
                     power=140,
                     speed=55,
                     vehicle_life=40,
                     gen=4,
                     intro_date=1940)

consist.add_unit(type=DieselRoadVehicle,
                 capacity=15,
                 vehicle_length=6)
