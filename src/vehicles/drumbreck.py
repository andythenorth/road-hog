import global_constants
from road_vehicle import Tanker

consist = Tanker(id = 'drumbreck',
                base_numeric_id = 800,
                title = 'Drumbreck [Tanker Tram]',
                roadveh_flag_tram = True,
                replacement_id = '-none',
                vehicle_life = 40,
                intro_date = 1870)

consist.add_unit(weight = 10,
                vehicle_length = 4,
                effects = ['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                always_use_same_spriterow = True)

consist.add_unit(weight = 5,
                capacity = 16,
                vehicle_length = 4,
                repeat = 3)

consist.add_model_variant(intro_date=0,
                          end_date=global_constants.max_game_date,
                          spritesheet_suffix=0,
                          graphics_processor=consist.graphics_processors[0])
