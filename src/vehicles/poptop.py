import global_constants
from road_vehicle import EdiblesTanker

consist = EdiblesTanker(id = 'poptop',
                        base_numeric_id = 780,
                        title = 'Poptop [Edibles Tanker Tram]',
                        tram_type = 'ELTR',
                        vehicle_life = 40,
                        intro_date = 1906)

consist.add_unit(capacity = 30,
                 vehicle_length = 8,
                 effects = ['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 repeat = 2)

consist.add_model_variant(intro_date=0,
                          end_date=global_constants.max_game_date,
                          spritesheet_suffix=0)
