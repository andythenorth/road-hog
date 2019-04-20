from road_vehicle import MailHauler, ElectricRoadVehicle

consist = MailHauler(id='foxley_mail',
                     base_numeric_id=190,
                     name='Foxley',
                     tram_type='ELRL',
                     power=240,  # custom HP
                     vehicle_life=40,
                     gen=4,                     intro_date=1903)

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=15,
                 vehicle_length=4,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 repeat=2)
