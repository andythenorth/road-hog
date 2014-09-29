import global_constants
from road_vehicle import EngineConsist, Tanker

consist = EngineConsist(id = 'oylbarral',
              base_numeric_id = 1020,
              title = 'Oylbarral [Tanker Tram]',
              roadveh_flag_tram = True,
              replacement_id = '-none',
              power = 150,
              vehicle_life = 40,
              intro_date = 1993)

consist.add_unit(Tanker(consist = consist,
                        weight = 20,
                        capacity = 20,
                        vehicle_length = 7,
                        visual_effect = 'VISUAL_EFFECT_DIESEL',
                        spriterow_num = 0), repeat=2)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
