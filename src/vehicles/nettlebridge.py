import global_constants
import graphics_processor.utils as graphics_utils
from road_vehicle import RVConsist, DumpHauler

consist = RVConsist(vehicle_type = DumpHauler,
                id = 'nettlebridge',
                base_numeric_id = 310,
                title = 'Nettlebridge [Dump Tram]',
                roadveh_flag_tram = True,
                replacement_id = '-none',
                vehicle_life = 40,
                intro_date = 1944)

consist.add_unit(weight = 12,
                capacity = 48,
                vehicle_length = 8,
                effects = ['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                repeat = 2)

graphics_processors = consist.get_graphics_processors(copy_block_top_offsets = [10],
                                                      paste_top_offset = 10)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0,
                       graphics_processor=graphics_processors[0])
