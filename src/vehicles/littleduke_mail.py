from road_vehicle import MailHauler, DieselRoadVehicle

consist = MailHauler(id='littleduke_mail',
                     base_numeric_id=270,
                     name='Littleduke',
                     power=380,
                     speed=90,
                     vehicle_life=40,
                     intro_date=1998)

consist.add_unit(type=DieselRoadVehicle,
                 capacity=25,
                 vehicle_length=6)
