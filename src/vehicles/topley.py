import global_constants
from road_vehicle import EngineConsist, PaxHauler

consist = EngineConsist(id = 'topley',
              base_numeric_id = 60,
              title = 'Topley [Bus]',
              replacement_id = '-none',
              power = 300,
              speed_dibble = 'plodding',
              vehicle_life = 40,
              intro_date = 1987)

consist.add_unit(PaxHauler(consist = consist,
                        weight = 25,
                        capacity = 90,
                        vehicle_length = 8,
                        visual_effect = 'VISUAL_EFFECT_DIESEL',
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
