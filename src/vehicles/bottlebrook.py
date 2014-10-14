import global_constants
from road_vehicle import EngineConsist, EdiblesTanker

consist = EngineConsist(id = 'bottlebrook',
              base_numeric_id = 970,
              title = 'Bottlebrook [Edibles Tanker Tram]',
              roadveh_flag_tram = True,
              replacement_id = '-none',
              power = 200,
              vehicle_life = 40,
              intro_date = 1905)

consist.add_unit(EdiblesTanker(consist = consist,
                        weight = 12,
                        capacity = 30,
                        vehicle_length = 7,
                        visual_effect = 'VISUAL_EFFECT_DIESEL',
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
