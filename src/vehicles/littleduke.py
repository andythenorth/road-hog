import global_constants
from road_vehicle import MailHauler

consist = MailHauler(id='littleduke',
                     base_numeric_id=270,
                     title='Littleduke [Courier Truck]',
                     power=380,
                     speed=90,
                     vehicle_life=40,
                     intro_date=1998)

consist.add_unit(capacity=25,
                 vehicle_length=6,
                 visual_effect='VISUAL_EFFECT_DIESEL')

consist.add_model_variant(spritesheet_suffix=0)
