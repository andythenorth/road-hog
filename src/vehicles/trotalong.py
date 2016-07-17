import global_constants
from road_vehicle import LivestockHauler

consist = LivestockHauler(id = 'trotalong',
                base_numeric_id = 720,
                title = 'Trotalong [Livestock Tram]',
                roadveh_flag_tram = True,
                replacement_id = '-none',
                vehicle_life = 40,
                intro_date = 1901)

consist.add_unit(weight = 12,
                capacity = 0,
                vehicle_length = 3,
                effects = ['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'])

consist.add_unit(weight = 4,
                capacity = 20,
                vehicle_length = 4,
                repeat = 3)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
