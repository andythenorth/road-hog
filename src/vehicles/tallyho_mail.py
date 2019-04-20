from road_vehicle import MailHauler, DieselRoadVehicle

consist = MailHauler(id='tallyho_mail',
                     base_numeric_id=450,
                     name='Tallyho',
                     power=90,
                     vehicle_life=40,
                     gen=4,
                     intro_date=1909)

consist.add_unit(type=DieselRoadVehicle,
                 capacity=15,
                 vehicle_length=6)
