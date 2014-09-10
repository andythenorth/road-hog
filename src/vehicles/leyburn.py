import global_constants
from road_vehicle import EngineConsist, PaxHauler

consist = EngineConsist(id = 'leyburn',
              base_numeric_id = 20,
              title = 'Leyburn [Bus]',
              replacement_id = '-none',
              power = 100,
              speed = 40,
              vehicle_life = 40,
              intro_date = 1920)

consist.add_unit(PaxHauler(consist = consist,
                        weight = 10,
                        capacity_pax = 30,
                        vehicle_length = 7,
                        visual_effect = 'VISUAL_EFFECT_DIESEL',
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
