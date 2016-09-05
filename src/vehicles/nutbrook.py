import global_constants
from road_vehicle import FruitHauler

consist = FruitHauler(id = 'nutbrook',
                base_numeric_id = 960,
                title = 'Nutbrook [Fruit Tram]',
                roadveh_flag_tram = True,
                replacement_id = '-none',
                vehicle_life = 40,
                intro_date = 1940)

consist.add_unit(weight = 15,
                capacity = 36,
                vehicle_length = 8,
                effects = ['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                repeat = 2)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)