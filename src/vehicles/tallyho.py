from road_vehicle import MailHauler

consist = MailHauler(id='tallyho',
                     base_numeric_id=450,
                     title='Tallyho [Courier Truck]',
                     power=90,
                     vehicle_life=40,
                     intro_date=1909)

consist.add_unit(capacity=15,
                 vehicle_length=6,
                 visual_effect='VISUAL_EFFECT_DIESEL')

consist.add_model_variant(spritesheet_suffix=0)
