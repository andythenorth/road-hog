import global_constants
from road_vehicle import LogHauler

consist = LogHauler(id='knockdown',
                    base_numeric_id=250,
                    title='Knockdown [Logging Truck]',
                    road_type='HAUL',
                    power=250,  # custom power
                    speed=50,
                    vehicle_life=40,
                    intro_date=1950)

consist.add_unit(capacity=30,
                 vehicle_length=7,
                 visual_effect='VISUAL_EFFECT_DIESEL')

consist.add_unit(capacity=30,
                 vehicle_length=6)

consist.add_model_variant(intro_date=0,
                          end_date=global_constants.max_game_date,
                          spritesheet_suffix=0)
