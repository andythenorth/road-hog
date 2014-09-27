import global_constants
from road_vehicle import EngineConsist, EdiblesTanker

consist = EngineConsist(id = 'silvertop',
              base_numeric_id = 960,
              title = 'Silvertop [Edibles Tanker Truck]',
              replacement_id = '-none',
              power = 200,
              vehicle_life = 40,
              intro_date = 1985)

consist.add_unit(EdiblesTanker(consist = consist,
                        weight = 7,
                        capacity_freight = 0,
                        vehicle_length = 7,
                        visual_effect = 'VISUAL_EFFECT_DIESEL',
                        spriterow_num = 0))

consist.add_unit(EdiblesTanker(consist = consist,
                        weight = 8,
                        capacity_freight = 56,
                        vehicle_length = 7,
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
