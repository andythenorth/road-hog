import global_constants
from road_vehicle import EdiblesTanker

consist = EdiblesTanker(id = 'bottlebrook',
                base_numeric_id = 510,
                title = 'Bottlebrook [Edibles Tanker Tram]',
                roadveh_flag_tram = True,
                replacement_id = '-none',
                vehicle_life = 40,
                intro_date = 1946)

consist.add_unit(weight = 18,
                capacity = 48,
                vehicle_length = 8,
                effects = ['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                repeat=2)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
