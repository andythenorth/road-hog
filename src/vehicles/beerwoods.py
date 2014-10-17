import global_constants
from road_vehicle import EngineConsist, EdiblesTanker

consist = EngineConsist(id = 'beerwoods',
              base_numeric_id = 420,
              title = 'Beerwoods [Edibles Tanker Truck]',
              replacement_id = '-none',
              power = 200,
              vehicle_life = 40,
              intro_date = 1945)

consist.add_unit(EdiblesTanker(consist = consist,
                        weight = 7,
                        capacity = 0,
                        vehicle_length = 7,
                        visual_effect = 'VISUAL_EFFECT_DIESEL',
                        spriterow_num = 0))

consist.add_unit(EdiblesTanker(consist = consist,
                        weight = 8,
                        capacity = 35,
                        vehicle_length = 7,
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
