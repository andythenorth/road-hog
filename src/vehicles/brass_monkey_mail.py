from road_vehicle import MailHauler

consist = MailHauler(id='brass_monkey_mail',
                     base_numeric_id=570,
                     name='Brass Monkey',
                     power=140,
                     speed=55,
                     vehicle_life=40,
                     intro_date=1940)

consist.add_unit(capacity=15,
                 vehicle_length=6,
                 visual_effect='VISUAL_EFFECT_DIESEL')

