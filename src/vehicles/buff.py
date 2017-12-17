import global_constants
from road_vehicle import LogHauler

consist = LogHauler(id='buff',
                    base_numeric_id=110,
                    title='Buff [Logging Truck]',
                    road_type='HAUL',
                    power=550,
                    speed=60,
                    vehicle_life=40,
                    intro_date=1994)

consist.add_unit(capacity=40,
                 vehicle_length=7,
                 visual_effect='VISUAL_EFFECT_DIESEL')

consist.add_unit(capacity=35,
                 vehicle_length=8)

consist.add_model_variant(intro_date=0,
                          end_date=global_constants.max_game_date,
                          spritesheet_suffix=0)
