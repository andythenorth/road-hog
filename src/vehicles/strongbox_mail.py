from road_vehicle import MailHauler, ElectricRoadVehicle

consist = MailHauler(id='strongbox_mail',
                     base_numeric_id=830,
                     name='Strongbox',
                     tram_type='ELRL',
                     power=480,  # custom power
                     vehicle_life=40,
                     gen=4,
                     intro_date=1961)

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=36,
                 vehicle_length=8,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'])
