import global_constants
from road_vehicle import RVConsist, PaxExpressHauler

consist = RVConsist(id = 'glenmore',
              base_numeric_id = 50,
              title = 'Glenmore [Coach]',
              replacement_id = '-none',
              power = 220,
              speed = 55,
              vehicle_life = 40,
              intro_date = 1935)

consist.add_unit(PaxExpressHauler(consist = consist,
                        weight = 20,
                        capacity = 30,
                        vehicle_length = 7,
                        visual_effect = 'VISUAL_EFFECT_DIESEL',
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
