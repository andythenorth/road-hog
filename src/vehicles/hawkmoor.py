import global_constants
from road_vehicle import DumpHauler

consist = DumpHauler(id = 'hawkmoor',
                base_numeric_id = 760,
                title = 'Hawkmoor [Dump Tram]',
                roadveh_flag_tram = True,
                replacement_id = '-none',
                vehicle_life = 40,
                intro_date = 1902)

consist.add_unit(weight = 12,
                capacity = 36,
                vehicle_length = 8,
                effects = ['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                repeat = 2)

graphics_processors = consist.get_graphics_processors(paste_top_offset = 10)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0,
                       graphics_processor=graphics_processors[0])
