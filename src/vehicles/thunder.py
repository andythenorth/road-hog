import global_constants
from road_vehicle import EngineConsist, PaxHauler

consist = EngineConsist(id = 'thunder',
              base_numeric_id = 40,
              title = 'Thunder [Bus]',
              replacement_id = '-none',
              power = 180,
              vehicle_life = 40,
              intro_date = 1940)

consist.add_unit(PaxHauler(consist = consist,
                        weight = 20,
                        capacity = 75,
                        vehicle_length = 7,
                        visual_effect = 'VISUAL_EFFECT_DIESEL',
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
