import global_constants
from road_vehicle import EngineConsist, LogHauler

consist = EngineConsist(id = 'buff',
              base_numeric_id = 110,
              title = 'Buff [Logging Truck]',
              replacement_id = '-none',
              power = 550,
              speed = 60,
              vehicle_life = 40,
              intro_date = 1994)

consist.add_unit(LogHauler(consist = consist,
                        weight = 10,
                        capacity = 30,
                        vehicle_length = 7,
                        visual_effect = 'VISUAL_EFFECT_DIESEL',
                        spriterow_num = 0))

consist.add_unit(LogHauler(consist = consist,
                        weight = 7,
                        capacity = 30,
                        vehicle_length = 8,
                        spriterow_num = 1))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
