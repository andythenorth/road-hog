from road_vehicle import MailHauler, DieselRoadVehicle

consist = MailHauler(id='goldmire_mail',
                     base_numeric_id=200,
                     name='Goldmire',
                     power=250,  # custom power
                     speed=75,
                     vehicle_life=40,
                     gen=4,                     intro_date=1971)

consist.add_unit(type=DieselRoadVehicle,
                 capacity=25,
                 vehicle_length=6)
