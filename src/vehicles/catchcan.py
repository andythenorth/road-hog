import global_constants
from road_vehicle import RVConsist, Tanker

consist = RVConsist(vehicle_type = Tanker,
                id = 'catchcan',
                base_numeric_id = 810,
                title = 'Catchcan [Tanker Tram]',
                roadveh_flag_tram = True,
                replacement_id = '-none',
                vehicle_life = 40,
                intro_date = 1902)

consist.add_unit(weight = 10,
                capacity = 24,
                vehicle_length = 6,
                effects = ['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'])

consist.add_unit(weight = 5,
                capacity = 24,
                vehicle_length = 4)

consist.add_unit(weight = 10,
                capacity = 24,
                vehicle_length = 6,
                effects = ['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'])

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
