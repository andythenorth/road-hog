import global_constants
from road_vehicle import RVConsist, LogHauler

consist = RVConsist(vehicle_type = LogHauler,
                id = 'knockdown',
                base_numeric_id = 250,
                title = 'Knockdown [Logging Truck]',
                replacement_id = '-none',
                power = 250, # custom power
                speed = 50,
                vehicle_life = 40,
                intro_date = 1950)

consist.add_unit(weight = 12,
                capacity = 30,
                vehicle_length = 7,
                visual_effect = 'VISUAL_EFFECT_DIESEL',
                spriterow_num = 0)

consist.add_unit(weight = 7,
                capacity = 30,
                vehicle_length = 6,
                spriterow_num = 3)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
