import global_constants
from road_vehicle import EngineConsist, RefrigeratedHauler

consist = EngineConsist(id = 'coldfall',
              base_numeric_id = 380,
              title = 'Coldfall [Reefer Truck]',
              replacement_id = '-none',
              power = 450,
              speed = 80,
              vehicle_life = 40,
              intro_date = 1982)

consist.add_unit(RefrigeratedHauler(consist = consist,
                        weight = 8,
                        capacity_freight = 0,
                        vehicle_length = 7,
                        visual_effect = 'VISUAL_EFFECT_DIESEL',
                        spriterow_num = 0))

consist.add_unit(RefrigeratedHauler(consist = consist,
                        weight = 10,
                        capacity_freight = 36,
                        vehicle_length = 7,
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
