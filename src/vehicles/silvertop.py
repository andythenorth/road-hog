import global_constants
from road_vehicle import RVConsist, EdiblesTanker

consist = RVConsist(vehicle_type = EdiblesTanker,
                id = 'silvertop',
                base_numeric_id = 380,
                title = 'Silvertop [Edibles Tanker Truck]',
                replacement_id = '-none',
                vehicle_life = 40,
                intro_date = 2001)

consist.add_unit(weight = 9,
                capacity = 20,
                vehicle_length = 5,
                effects = ['EFFECT_SPRITE_DIESEL, -3, 1, 10'])

consist.add_unit(weight = 9,
                capacity = 20,
                vehicle_length = 4)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
