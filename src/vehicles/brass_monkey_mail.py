from road_vehicle import MailHauler, DieselRoadVehicle

consist = MailHauler(id='brass_monkey_mail',
                     base_numeric_id=570,
                     name='Brass Monkey',
                     power=140,
                     speed=55,
                     vehicle_life=40,
                     gen=3,
                     intro_date_offset=1)  # introduce later than gen epoch by design

consist.add_unit(type=DieselRoadVehicle,
                 capacity=15,
                 vehicle_length=6)
