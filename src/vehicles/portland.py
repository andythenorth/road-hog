import global_constants
from road_vehicle import OpenHauler

consist = OpenHauler(id = 'portland',
                base_numeric_id = 860,
                title = 'Portland [Open Tram]',
                roadveh_flag_tram = True,
                replacement_id = '-none',
                vehicle_life = 40,
                intro_date = 1900,)

consist.add_unit(weight = 12,
                capacity = 48,
                vehicle_length = 8,
                cargo_length = 3,
                effects = ['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'])

consist.add_unit(weight = 4,
                capacity = 24,
                vehicle_length = 4,
                cargo_length = 3)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0,
                       graphics_processor=consist.graphics_processors[0])
